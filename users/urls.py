from django.urls import path

from .views import custom_signup, custom_login, custom_logout, set_username

urlpatterns = [
    path('signup/', custom_signup, name='custom_signup'),
    path('login/', custom_login, name='custom_login'),
    path('logout/', custom_logout, name='logout'),
    path("set-username/", set_username, name="set_username"),
]
