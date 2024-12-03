from django.http import Http404

from .forms import IdeaForm, SignUpForm
from .models import Idea
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount

def home(request):
    return render(request, 'home.html')  # Render a homepage template

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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            # Log the user in after successful signup
            login(request, user)
            messages.success(request, "Signup successful! Welcome to Scidea.")
            return redirect('home')  # Redirect to homepage after successful signup
        else:
            messages.error(request, "There was an error with your signup. Please try again.")
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


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
