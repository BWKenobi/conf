from django.urls import path
from django.conf.urls import url
from .views import view_user, view_edit_profile

urlpatterns = [
	path('view_edit_profile', view_edit_profile, name = 'view_edit_profile'),
	path('view_user/<int:pk>/', view_user, name = 'view_user'),
]