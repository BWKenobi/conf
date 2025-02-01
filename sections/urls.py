from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.urls import include
from django.contrib.auth import views as auth_views

from .views import sections, add_section, edit_section


urlpatterns = [
	path('', sections, name = 'sections'),
	path('add_section', add_section, name = 'add_section'),
	path('edit_section/<int:pk>', edit_section, name = 'edit_section'),
]