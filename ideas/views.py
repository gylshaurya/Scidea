from django.shortcuts import render, redirect
from .forms import IdeaForm
from .models import Idea
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful signup
            return redirect('/')  # Redirect to the home page or wherever you prefer
    else:
        form = UserCreationForm()
    
    # Explicitly specify the template path
    return render(request, 'registration/signup.html', {'form': form})