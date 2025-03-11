from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_tab, name='profile_tab'),
    path('activity/', views.activity_tab, name='activity_tab'),
    path('lists/', views.lists_tab, name='lists_tab'),
    path('settings/', views.settings_tab, name='settings_tab'),
]