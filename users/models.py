import cloudinary.models
from django.contrib.auth.models import BaseUserManager, AbstractUser
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
    profile_picture = cloudinary.models.CloudinaryField('image', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)  # Already in AbstractUser

    bio = models.TextField(blank=True, null=True)
    interest_tags = models.ManyToManyField("ideas.Tag", blank=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)


    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_profile_picture(self):
        """Return profile picture URL or default Google picture or default avatar."""
        if self.profile_picture:
            return self.profile_picture.url  # ✅ Cloudinary image
        if hasattr(self, 'socialaccount_set') and self.socialaccount_set.exists():
            return self.socialaccount_set.first().extra_data.get("picture")  # ✅ Google image
        return "/static/default-avatar.svg"  # ✅ Default avatar

    def __str__(self):
        return self.email



