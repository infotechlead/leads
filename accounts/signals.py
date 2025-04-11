from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Safely try to save the profile only if it exists
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # For users created before signals were added
        Profile.objects.create(user=instance)
