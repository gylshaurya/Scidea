from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/upvote/', views.toggle_upvote, name='toggle_upvote'),
    path('profile/<str:username>/', views.profile_view, name='profile_tab'),
    path('profile/<str:username>/<str:tab>/', views.profile_view, name='profile_tab_specific'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('support/', views.support, name='support'),
    path('feedback/', views.feedback, name='feedback'),
    path('settings/', views.settings, name='settings'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
