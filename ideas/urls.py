from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_idea, name='submit_idea'),
    path('list/', views.idea_list, name='idea_list'),
]   
