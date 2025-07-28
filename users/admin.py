from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    def profile_picture_display(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="40px" height="40px" style="border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return "No Picture"

    profile_picture_display.short_description = "Profile Picture"

    list_display = ("email", "name", "username", "profile_picture_display", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "username", "profile_picture")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "name", "username", "profile_picture", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email", "username")
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
