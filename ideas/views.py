from django.contrib.auth.hashers import make_password
from django.http import Http404

from .forms import IdeaForm, CustomSignupForm
from .models import Idea, CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def home(request):
    ideas = Idea.objects.all()
    return render(request, 'home.html', {'ideas': ideas})  # Render a homepage template

def profile_view(request, pk):
    user = CustomUser.objects.get(pk=pk)
    return render(request, 'profile.html', {'user': user})

def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    return render(request, 'idea_detail.html', {'idea': idea})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required()
def custom_logout_view(request):
    if request.method == 'GET':
        logout(request)  # Logs out the user
        return redirect('/')  # Redirect to home page or any desired page

@login_required
def submit_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.author = request.user  # Assign the logged-in user as the author
            idea.save()
            return redirect('idea_list')  # Redirect to the idea list page
    else:
        form = IdeaForm()
    return render(request, 'ideas/submit_idea.html', {'form': form})

def idea_list(request):
    query = request.GET.get('q', '')
    if query:
        ideas = Idea.objects.filter(title__icontains=query)
    else:
        ideas = Idea.objects.all()
    return render(request, 'ideas/idea_list.html', {'ideas': ideas})

def get_profile_picture(request):
    if request.user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=request.user).first()
        if social_account:
            profile_picture = social_account.get_avatar_url()  # Google profile picture URL
            return profile_picture
    return None

def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', pk=user.pk)  # Redirect to the profile page
    else:
        form = CustomSignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the email is already registered
        if CustomUser.objects.filter(email=email).exists():  # Use CustomUser here
            return render(request, 'registration/signup.html', {'error': 'Email already registered!'})

        # Create and save the user
        user = CustomUser.objects.create(
            username=name,
            email=email,
            password=make_password(password)
        )
        return render(request, 'registration/login.html')  # Redirect to login page after successful signup

    return render(request, 'registration/signup.html')
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to home page after successful login
        else:
            messages.error(request, "We couldn’t find an account matching the username and password.")

    return render(request, 'registration/login.html')

@login_required
def profile_tab(request):
    return render(request, 'tabs/profile_tab.html')

@login_required
def activity_tab(request):
    return render(request, 'tabs/activity_tab.html')

@login_required
def lists_tab(request):
    return render(request, 'tabs/lists_tab.html')

@login_required
def settings_tab(request):
    return render(request, 'tabs/settings_tab.html')
