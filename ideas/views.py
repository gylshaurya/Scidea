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

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages


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



def guidelines(request):
    return render(request, 'extras/guidelines.html', {})

def support(request):
    return render(request, 'extras/support.html', {})

from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect

def feedback(request):
    if request.method == 'POST':
        email = request.POST.get('email', 'No email provided')
        form_type = None
        subject = ''
        message_body = ''

        # Identify which form was submitted
        if 'message' in request.POST and 'description' not in request.POST:
            form_type = 'User General Feedback'
            subject = f"{form_type}"
            message_body = request.POST.get('message')

        elif 'description' in request.POST:
            form_type = 'Bug Report'
            subject = f"User Bug Report"
            message_body = request.POST.get('description')

        elif 'idea' in request.POST:
            form_type = 'Feature Suggestion'
            subject = f"User Feature Suggestion"
            message_body = request.POST.get('idea')

        else:
            messages.error(request, "Unknown form submitted.")
            return redirect('feedback')

        # Construct email content
        email_content = f"{message_body}"

        # Prepare email
        email_obj = EmailMessage(
            subject=subject,
            body=email_content,
            from_email='scidea.mail@gmail.com',
            to=['scidea.mail@gmail.com'],
            reply_to=[email] if email else None,
        )

        # Handle multiple attachments
        files = request.FILES.getlist('attachments')
        for f in files:
            email_obj.attach(f.name, f.read(), f.content_type)

        try:
            email_obj.send()
            messages.success(request, "Thank you! Your feedback has been sent.")
        except Exception as e:
            print("Email sending error:", e)
            messages.error(request, "There was an error sending your feedback. Please try again later.")

        return redirect('feedback')

    return render(request, 'extras/feedback.html')



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

            selected_tag_ids = request.POST.getlist("selected_tags[]")

            if selected_tag_ids:
                post.tags.set(selected_tag_ids)
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