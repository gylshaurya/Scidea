from django.contrib.auth.models import BaseUserManager
import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    google_profile_picture = models.URLField(blank=True, null=True)  # Store Google profile pic

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_profile_picture(self):
        """Return profile picture, fallback to Google pic, or generate initials image."""
        if self.profile_picture:
            return self.profile_picture.url
        elif self.google_profile_picture:
            return self.google_profile_picture
        else:
            return f"/static/initials/{self.generate_initials()}.png"

    def generate_initials(self):
        """Generate initials-based image (e.g., 'AB.png')."""
        initials = "".join([word[0] for word in (self.name or "User").split() if word][:2]).upper()
        if not initials:
            initials = ''.join(random.choices(string.ascii_uppercase, k=2))
        return initials

