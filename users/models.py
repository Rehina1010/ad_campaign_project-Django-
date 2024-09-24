from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True, blank=False)
    is_active = models.BooleanField(default=False)
    group_id = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('user', 'User')])
    avatar_url = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, help_text="Bio or additional information about the user.")
    location = models.CharField(max_length=30, blank=True, help_text="User's location.")
    birth_date = models.DateField(null=True, blank=True, help_text="User's birth date.")

    def __str__(self):
        return self.user.username
