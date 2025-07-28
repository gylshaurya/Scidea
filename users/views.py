import cloudinary.uploader
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model, authenticate, get_backends
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import CustomUser


def custom_signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email is already registered
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "You already have an account with this email id")

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
    messages.error(request, "")
    return render(request, "registration/signup.html")


def custom_login(request):
    messages.error(request, "")
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
        profile_picture = request.FILES.get("profile_picture")

        if username:
            user.username = username

        if profile_picture:
            #Upload to Cloudinary
            uploaded_image = cloudinary.uploader.upload(profile_picture)
            user.profile_picture = uploaded_image["url"]

        #If logged in via Google and name not set, fetch from Google profile
        if not user.name and hasattr(user, 'socialaccount_set') and user.socialaccount_set.exists():
            social_data = user.socialaccount_set.first().extra_data
            user.name = (
                social_data.get("name") or
                social_data.get("given_name") or
                ""
            )

        user.save()

        return redirect("home")

    # For displaying Google profile picture in the form (read-only usage)
    google_profile_picture = None
    if hasattr(user, 'socialaccount_set') and user.socialaccount_set.exists():
        google_profile_picture = user.socialaccount_set.first().extra_data.get("picture")

    return render(request, "registration/set_username.html", {
        "user": user,
        "google_profile_picture": google_profile_picture,
    })

def check_username(request):
    username = request.GET.get("username", "").strip()

    # Check if the username is empty
    if not username:
        return JsonResponse({"error": "Username cannot be empty"}, status=400)

    # Check if the username already exists
    is_taken = CustomUser.objects.filter(username__iexact=username).exists()

    return JsonResponse({"available": not is_taken})