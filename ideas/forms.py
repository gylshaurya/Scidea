from django import forms
from .models import Idea
from django.contrib.auth.models import User

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'content']


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']  # You can customize the fields as needed

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords don't match.")
        return password_confirm