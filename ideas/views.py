from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Value, BooleanField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import Post, Tag, Upvote


def home(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(status='published').order_by('-created_at')

    if query:
        posts = posts.filter(tags__name__icontains=query).distinct()

    # Annotate each post with whether the current user has upvoted it
    if request.user.is_authenticated:
        upvote_subquery = Upvote.objects.filter(user=request.user, post=OuterRef('pk'))
        posts = posts.annotate(upvoted=Exists(upvote_subquery))
    else:
        posts = posts.annotate(upvoted=Value(False, output_field=BooleanField()))

    tags = Tag.objects.all()
    return render(request, 'home.html', {'posts': posts, 'tags': tags})


@login_required
def create_post(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'published' if 'publish' in request.POST else 'draft'
            post.save()

            selected_tag_ids = request.POST.get('selected_tags', '')
            if selected_tag_ids:
                tag_id_list = [tag_id for tag_id in selected_tag_ids.split(',') if tag_id.isdigit()]
                tag_objects = Tag.objects.filter(id__in=tag_id_list)
                post.tags.set(tag_objects)
            else:
                post.tags.clear()  # Just to be safe

            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'ideas/create_post.html', {'form': form, 'tags': tags})

# Post detail view
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    upvoted = Upvote.objects.filter(post=post, user=request.user).exists()

    return render(request, 'ideas/post_detail.html', {
        'post': post,
        'upvoted': upvoted,
    })

@require_POST
@login_required
def toggle_upvote(request, post_id):
    post = Post.objects.get(pk=post_id)
    upvote, created = Upvote.objects.get_or_create(user=request.user, post=post)

    if not created:
        upvote.delete()
        upvoted = False
    else:
        upvoted = True

    return JsonResponse({
        'upvoted': upvoted,
        'count': Upvote.objects.filter(post=post).count()
    })


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