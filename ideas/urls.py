from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import path, include

from . import views

urlpatterns = [
    path('submit/', views.submit_idea, name='submit_idea'),
    path('list/', views.idea_list, name='idea_list'),
    path('login/', views.custom_login, name='custom_login'),
    path('signup/', views.signup, name='signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view
    path('accounts/', include('allauth.urls')),
    path('profile/', views.profile, name='profile'),
    path('tabs/profile/', views.profile_tab, name='profile_tab'),
    path('tabs/activity/', views.activity_tab, name='activity_tab'),
    path('tabs/lists/', views.lists_tab, name='lists_tab'),
    path('tabs/settings/', views.settings_tab, name='settings_tab'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
