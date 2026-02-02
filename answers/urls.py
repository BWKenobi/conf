from django.urls import path
from django.conf.urls import url
from .views import view_my_answers, get_answers, get_answer

urlpatterns = [
	path('view_my_answers', view_my_answers, name = 'view_my_answers'),
	path('get_answers', get_answers, name = 'get_answers'),
]


urlpatterns += [
	path('ajax/get_answer', get_answer, name = 'ajax_get_answer'),
]