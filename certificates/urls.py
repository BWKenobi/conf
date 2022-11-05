from django.urls import path
from django.conf.urls import url
from .views import del_serificates, send_serificates, generate_sertificates

urlpatterns = [
	path('del_serificates', del_serificates, name = 'del_serificates'),
	path('send_serificates', send_serificates, name = 'send_serificates'),
]

urlpatterns += [
	path('ajax/generate-sertificates/', generate_sertificates, name = 'generate_sertificates'),
]
