from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Value, BooleanField, Count, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.cache import cache

from users.models import CustomUser
from .forms import PostForm, CommentForm, EditProfileForm
from .models import Post, Tag, Upvote, Comment


def home(request):
    tag_id = request.GET.get('tag')
    query = request.GET.get('q')

    posts = Post.objects.filter(status='published').annotate(
        comment_count=Count('comments'),
    )

    if query == 'popular':
        posts = posts.annotate(upvote_count=Count('upvotes')).order_by('-upvote_count', '-created_at')
    elif tag_id:
        posts = posts.filter(tags__id=tag_id).distinct()
    else:
        posts = posts.order_by('-created_at')

    # Optimization: prefetch author, tags, upvotes
    posts = posts.select_related('author').prefetch_related('tags', 'upvotes')

    # Annotate upvoted status
    if request.user.is_authenticated:
        upvote_subquery = Upvote.objects.filter(user=request.user, post=OuterRef('pk'))
        posts = posts.annotate(upvoted=Exists(upvote_subquery))
    else:
        posts = posts.annotate(upvoted=Value(False, output_field=BooleanField()))

    # Cache tag list for 1 hour
    tags = cache.get('all_tags')
    if not tags:
        tags = Tag.objects.all()
        cache.set('all_tags', tags, 60 * 60)

    return render(request, 'home.html', {'posts': posts, 'tags': tags, 'selected_tag_id': tag_id})




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


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    upvoted = Upvote.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect(f"{reverse('post_detail', kwargs={'pk': pk})}#comments")
    else:
        form = CommentForm()

    return render(request, 'ideas/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
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






def profile_view(request, username, tab="about"):
    user_profile = get_object_or_404(CustomUser, username=username)
    user_posts = Post.objects.filter(author=user_profile, status='published')

    is_owner = request.user == user_profile

    total_ideas = user_posts.count()

    # Count upvotes across all of user's posts
    total_upvotes = Upvote.objects.filter(post__in=user_posts).count()

    # Count comments across all of user's posts
    total_comments = Comment.objects.filter(post__in=user_posts).count()

    context = {
        'user_profile': user_profile,
        'is_owner': is_owner,
        'active_tab': tab,
        'total_ideas': total_ideas,
        'total_upvotes': total_upvotes,
        'total_comments': total_comments,
    }

    # Load data for each tab
    if tab == "about":
        template = "profile/about_tab.html"

    elif tab == "activity":
        comments = Comment.objects.filter(user=user_profile)
        upvotes = Upvote.objects.filter(user=user_profile)
        posts = Post.objects.filter(author=user_profile, status='published')
        context.update({'comments': comments, 'upvotes': upvotes, 'posts': posts})
        template = "profile/activity_tab.html"

    elif tab == "ideas":
        posts = Post.objects.filter(author=user_profile, status='published')
        context.update({'posts': posts})
        template = "profile/ideas_tab.html"

    elif tab == "bookmarks" and is_owner:
        bookmarks = ...  # Fetch bookmarked posts
        context.update({'bookmarks': bookmarks})
        template = "profile/bookmarks_tab.html"

    elif tab == "drafts" and is_owner:
        drafts = Post.objects.filter(author=user_profile, status='draft')
        context.update({'drafts': drafts})
        template = "profile/drafts_tab.html"

    else:
        template = "profile/about_tab.html"

    return render(request, "profile/profile.html", {**context, 'tab_template': template})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'profile/edit_profile.html', {'form': form})