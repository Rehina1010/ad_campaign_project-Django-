from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

User = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=SocialAccount)
def update_user_from_social_account(sender, instance, **kwargs):
    user = instance.user
    if instance.provider == 'google':
        extra_data = instance.extra_data
        user.first_name = extra_data.get('given_name', '')
        user.last_name = extra_data.get('family_name', '')
        user.username = extra_data.get('name', user.first_name)
        user.is_active = True
        user.save()


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    if user.is_authenticated and user.is_active:
        pass
