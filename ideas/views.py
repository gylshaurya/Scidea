from .forms import IdeaForm, SignUpForm
from .models import Idea
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    return render(request, 'home.html')  # Render a homepage template

@login_required
def profile(request):
    user_ideas = Idea.objects.filter(author=request.user)
    return render(request, 'profile.html', {'user_ideas': user_ideas})

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


def user_profile(request):
    # Accessing the current logged-in user's data
    user = request.user

    # If the user is authenticated
    if user.is_authenticated:
        # Accessing user data
        username = user.username
        email = user.email
        first_name = user.first_name
        last_name = user.last_name

        # Render a profile page with user data
        return render(request, 'profile.html',
                      {'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})
    else:
        # If not authenticated, redirect to log in
        return redirect('login')