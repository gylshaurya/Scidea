"""
URL configuration for Scidea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect


def custom_logout_view(request):
    if request.method == 'GET':
        logout(request)  # Logs out the user
        return redirect('/')  # Redirect to home page or any desired page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', __import__('ideas.views').views.profile, name='profile'),
    path('ideas/', include('ideas.urls')),  # Include the URLs for the ideas app
    path('', __import__('ideas.views').views.home, name='home'),
    path('signup/', __import__('ideas.views').views.signup, name='signup'),
    path('login/', include('django.contrib.auth.urls')),  # Django handles login via this
    path('logout/', custom_logout_view, name='logout'),
]



