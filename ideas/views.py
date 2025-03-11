from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ideas.forms import PostForm


def home(request):
    return render(request, 'home.html')


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign logged-in user as the author
            post.save()
            form.save_m2m()  # Save the many-to-many tags
            return redirect('home')  # Redirect to homepage after submission
    else:
        form = PostForm()

    return render(request, 'ideas/create_post.html', {'form': form})





@login_required
def profile_tab(request):
    return render(request, 'profile_tabs/profile_tab.html')

@login_required
def activity_tab(request):
    return render(request, 'profile_tabs/activity_tab.html')

@login_required
def lists_tab(request):
    return render(request, 'profile_tabs/lists_tab.html')

@login_required
def settings_tab(request):
    return render(request, 'profile_tabs/settings_tab.html')