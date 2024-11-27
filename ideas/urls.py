from django.urls import path
from . import views
from .views import custom_login

urlpatterns = [
    path('submit/', views.submit_idea, name='submit_idea'),
    path('list/', views.idea_list, name='idea_list'),
    path('login/', custom_login, name='custom_login'),
]   
