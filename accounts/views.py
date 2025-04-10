from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .forms import LoginForm, EntryForm, SubUserCreationForm, ProfileForm
from .models import Entry, CustomUser
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import IntegrityError
from datetime import datetime,time,date,timedelta




User = get_user_model()

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                return render(request, "login.html", {"form": form, "error": "Invalid username or password"})
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

@login_required
def dashboard(request):
    entries = Entry.objects.filter(user=request.user).order_by("-date")
    return render(request, 'dashboard.html', {'entries': entries})

def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('create_entry')
    else:
        form = EntryForm()
    return render(request, 'create_entry.html', {'form': form})

@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    original_user = entry.user  # ✅ Preserve the original user

    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = original_user  # ✅ Restore the user so it's not overwritten
            entry.last_edited_by = request.user
            entry.last_edited_at = now()
            entry.save()
            return redirect(f"{reverse('entry_list')}?start_date={entry.date}&end_date={entry.date}")
    else:
        form = EntryForm(instance=entry)

    return render(request, 'edit_entry.html', {'form': form})

@login_required
def entry_list(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filter_user_id = request.GET.get('filter_user')

    # Determine the user scope
    users = [request.user]
    subusers = []
    if not request.user.is_subuser:
        subusers = CustomUser.objects.filter(parent_user=request.user, is_subuser=True)
        users += list(subusers)

    # Base query
    entries = Entry.objects.filter(user__in=users)

    # Filter by specific user (admin use case)
    if filter_user_id:
        entries = entries.filter(user_id=filter_user_id)

    # Search by field
    if field and value:
        filter_kwargs = {f"{field}__icontains": value}
        entries = entries.filter(**filter_kwargs)

    # Date range filter (optional, no default to today)
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            entries = entries.filter(date__gte=start)
        except ValueError:
            messages.error(request, "Invalid start date format.")
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            entries = entries.filter(date__lte=end)
        except ValueError:
            messages.error(request, "Invalid end date format.")

    entries = entries.order_by("-date")

    return render(request, "entry_list.html", {
        "entries": entries,
        "field": field,
        "value": value,
        "start_date": start_date,
        "end_date": end_date,
        "filter_user_id": filter_user_id,
        "subusers": subusers,
    })

@login_required
def create_subuser(request):
    subusers = CustomUser.objects.filter(parent_user=request.user, is_subuser=True)
    if request.method == 'POST':
        user_form = SubUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another.")
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please use a different email address.")
            else:
                try:
                    subuser = user_form.save(commit=False)
                    subuser.parent_user = request.user
                    subuser.is_subuser = True
                    subuser.set_password(user_form.cleaned_data["password1"])  # ✅ Important
                    subuser.save()

                    profile = profile_form.save(commit=False)
                    profile.user = subuser
                    profile.parent_user = request.user
                    profile.save()

                    messages.success(request, "Subuser created successfully.")
                    user_form = SubUserCreationForm()
                    profile_form = ProfileForm()
                    subusers = CustomUser.objects.filter(parent_user=request.user, is_subuser=True)
                except IntegrityError as e:
                    print("Integrity Error:", e)
                    messages.error(request, "Something went wrong while creating the subuser.")
        else:
            messages.error(request, "Please correct the highlighted errors below.")
    else:
        user_form = SubUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'create_subuser.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'subusers': subusers,
    })



@login_required
def toggle_subuser_status(request, user_id):
    user = CustomUser.objects.filter(id=user_id, parent_user=request.user, is_subuser=True).first()
    if user:
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"Subuser '{user.username}' has been {status}.")
    else:
        messages.error(request, "Subuser not found or not authorized.")
    return redirect('create_subuser')  # redirect to the subuser list page



@login_required
def reports_view(request):
    user = request.user
    entries = Entry.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    field = request.GET.get('field')
    value = request.GET.get('value')

    # Filter for subuser/admin access
    if user.is_subuser:
        entries = entries.filter(user=user)
    else:
        entries = entries.filter(Q(user=user) | Q(user__parent_user=user))

    # Optional date filters
    if start_date:
        try:
            entries = entries.filter(date__gte=datetime.strptime(start_date, "%Y-%m-%d"))
        except ValueError:
            messages.error(request, "Invalid start date format.")

    if end_date:
        try:
            entries = entries.filter(date__lte=datetime.strptime(end_date, "%Y-%m-%d"))
        except ValueError:
            messages.error(request, "Invalid end date format.")

    # Optional field search
    if field and value:
        filter_kwargs = {f"{field}__icontains": value}
        entries = entries.filter(**filter_kwargs)

    entries = entries.order_by("-date")

    return render(request, 'reports.html', {
        'entries': entries,
        'start_date': start_date,
        'end_date': end_date,
        'field': field,
        'value': value,
    })


@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    # Check permissions
    if request.user != entry.user and request.user != entry.user.parent_user:
        return redirect("entry_list")  # deny access

    entry.delete()
    return redirect("entry_list")


# def create_super_user(request):
#     User = get_user_model()
#     if not User.objects.filter(username='admin').exists():
#         User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
#         return HttpResponse("✅ Superuser created.")
#     return HttpResponse("⚠️ Superuser already exists.")