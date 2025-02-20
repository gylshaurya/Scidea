from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Idea

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('name', 'profile_picture', 'bio')}),
    )

admin.site.register(Idea)
