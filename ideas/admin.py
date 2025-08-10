from django.contrib import admin
from .models import Post, Tag, Upvote, Comment

class CommentInline(admin.TabularInline):  # or admin.StackedInline if you want more space
    model = Comment
    extra = 0  # don't show extra blank comment forms
    readonly_fields = ('user', 'content', 'created_at')
    can_delete = False

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'tags')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)
    inlines = [CommentInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')

# Do NOT register Comment separately anymore
# admin.site.register(Comment)  <- REMOVE this if it exists
