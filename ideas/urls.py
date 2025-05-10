from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/upvote/', views.toggle_upvote, name='toggle_upvote'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
