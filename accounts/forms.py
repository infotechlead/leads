# accounts/forms.py
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()  # <- This fetches your CustomUser model
from django import forms
from .models import Profile
from .models import Entry
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'organization_name', 'mobile_number', 'address',
            'pan_number', 'gstin_number', 'country', 'state', 'city', 'pin_code'
        ]

        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),} 

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'address':  # Already set in widgets
                 field.widget.attrs['class'] = 'form-control'
            field.label_suffix = ''

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ['user', 'last_edited_by', 'last_edited_at']    
    
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'executive': forms.TextInput(attrs={'class': 'form-control'}),
            'party_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control',"pattern": "[0-9]{10}"}),
            'model': forms.TextInput(attrs={'class': 'form-control',}),
            'sr_no': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'requirement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quote_amt': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'confirmation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class SubUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # ✅ Important
        fields = ['username', 'email' ,'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SubUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.label_suffix = ''
