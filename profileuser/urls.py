from django.urls import path
from django.conf.urls import url
from .views import view_edit_profile

urlpatterns = [
	path('view_edit_profile', view_edit_profile, name = 'view_edit_profile'),
]