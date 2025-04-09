# accounts/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# ⬅️ Put this FIRST
class CustomUser(AbstractUser):
    parent_user = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='created_users')
    is_subuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Then define the other models
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    parent_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='subusers')
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True, unique=True)
    gstin_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    entry_no = models.AutoField(primary_key=True)
    date = models.DateField(null=True, blank=True)
    last_edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_entries')
    last_edited_at = models.DateTimeField(null=True, blank=True)
    client_name = models.CharField(max_length=255)
    executive = models.CharField(max_length=255)
    party_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)
    model = models.CharField(max_length=255,null=True, blank=True)
    sr_no = models.CharField(max_length=255,null=True, blank=True)
    type = models.CharField(max_length=255)
    requirement = models.CharField(max_length=255)
    quote_amt = models.CharField(max_length=255)
    cost = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Drop', 'Drop'),
            ('Done', 'Done'),
        ],
        default='Pending'
    )
    confirmation_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return f"Entry {self.entry_no} - {self.client_name}"
