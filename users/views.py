from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model, authenticate, get_backends
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import CustomUser


def custom_signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email is already registered
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken!")
            return redirect("custom_signup")

        # Create and save the user
        user = CustomUser(email=email, name=name)
        user.save()

        # Set and save the hashed password
        user.set_password(password)
        user.save(update_fields=["password"])  # Save only the password field

        # 🔥 Authenticate user explicitly using the backend
        backend = get_backends()[0]  # Get the first configured backend
        user = authenticate(request, email=email, password=password)  # Try authentication

        if user is not None:
            login(request, user, backend=f"{backend.__module__}.{backend.__class__.__name__}")
            return redirect("set_username")

        messages.error(request, "Authentication failed. Try logging in manually.")
        return redirect("custom_login")

    return render(request, "registration/signup.html")


def custom_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)  # Use authenticate()

        if user is not None:
            login(request, user)  # No need to manually set backend
            return redirect("/")
        else:
            try:
                user = CustomUser.objects.get(email=email)

                # Only check `has_usable_password()` AFTER failing authentication
                if not user.has_usable_password():
                    messages.error(request, "You signed up using Google. Please log in with Google.")
                else:
                    messages.error(request, "Invalid Password")
            except CustomUser.DoesNotExist:
                messages.error(request, "No account found with this email.")

            return render(request, "registration/login.html")

    return render(request, "registration/login.html")

def custom_logout(request):
    """Logs out the user and redirects to home."""
    logout(request)
    return redirect('/')

User = get_user_model()

@login_required
def set_username(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        profile_picture = request.FILES.get("profile_picture")  # Get uploaded file

        if not username:
            messages.error(request, "Username is required.")
            return redirect("set_username")

        if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "Username is already taken!")
            return redirect("set_username")

        user.username = username

        # Save uploaded profile picture if available
        if profile_picture:
            user.profile_picture = profile_picture

        user.save()
        return redirect("/")  # Redirect home after setup

    google_login = bool(user.google_profile_picture)  # Check if logged in via Google

    return render(request, "registration/set_username.html", {"google_login": google_login, "user": user})

def google_login_redirect(request):
    """After Google login, check if the user needs to set a username."""
    user = request.user
    if not user.username:
        # Get Google profile picture
        social_account = SocialAccount.objects.filter(user=user, provider="google").first()
        if social_account:
            google_profile_picture = social_account.extra_data.get("picture", "")
            user.google_profile_picture = google_profile_picture
            user.save()

        return redirect("set_username")  # Redirect to username setup
    return redirect("/")  # Redirect home if username exists