from django.urls import path
from django.conf.urls import url
from .views import view_coprofiles, add_coprofile, del_coprofile, edit_coprofile

urlpatterns = [
	path('view_coprofiles', view_coprofiles, name = 'view_coprofiles'),
	path('add_coprofile', add_coprofile, name = 'add_coprofile'),
	path('del_coprofile/<int:pk>', del_coprofile, name = 'del_coprofile'),
	path('edit_coprofile/<int:pk>', edit_coprofile, name = 'edit_coprofile'),
]