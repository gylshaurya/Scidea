from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import create_post

urlpatterns = [
    path('', views.home, name='home'),  # Set homepage route
    path('create/', create_post, name='create_post')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
