from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.urls import include
from django.contrib.auth import views as auth_views

from .views import send_info_message


urlpatterns = [
	path('send_info_message', send_info_message, name = 'send_info_message'),
]