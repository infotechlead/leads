# accounts/admin.py
from django.contrib import admin
from .models import Profile
from .models import Entry
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class ProfileAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set on create
            obj.parent_user = request.user
        obj.save()
    list_display = (
        'user', 'parent_user', 'organization_name', 'mobile_number',
        'pan_number', 'gstin_number', 'country', 'state', 'city', 'pin_code'
    )
    # readonly_fields = ('parent_user',)  # ✅ Make it read-only
    search_fields = (
        'user__username', 'user__email', 'pan_number',
        'gstin_number', 'organization_name'
    )

admin.site.register(Profile, ProfileAdmin)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('entry_no', 'date', 'client_name', 'executive', 'status')
    search_fields = ('entry_no', 'client_name', 'executive')
    list_filter = ('status', 'confirmation_date')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('parent_user',)}),
    )
    list_display = UserAdmin.list_display + ('parent_user',)    

