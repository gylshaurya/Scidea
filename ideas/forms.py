from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Idea, CustomUser
from django.contrib.auth.models import User

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'content']


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'password1', 'password2', 'profile_picture']