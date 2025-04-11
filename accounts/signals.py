# accounts/signals.py
from django.db.models.signals import post_save,pre_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

User = get_user_model()

@receiver(pre_save, sender=User)
def lowercase_username(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
