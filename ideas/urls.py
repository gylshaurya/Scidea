from django.urls import path, include
from . import views
from .views import custom_login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('submit/', views.submit_idea, name='submit_idea'),
    path('list/', views.idea_list, name='idea_list'),
    path('login/', views.custom_login, name='custom_login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view
    path('accounts/', include('allauth.urls')),

]   
