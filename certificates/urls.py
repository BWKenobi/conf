from django.urls import path
from django.conf.urls import url
from .views import generate_sertificates

urlpatterns = [
	path('ajax/generate-sertificates/', generate_sertificates, name = 'generate_sertificates'),
]
