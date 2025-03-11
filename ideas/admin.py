from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
from .models import Post, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(CustomUser, UserAdmin)
