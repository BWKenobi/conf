from django.urls import path
from django.conf.urls import url
from .views import view_coprofiles, add_coprofile, del_coprofile, edit_coprofile, add_report_file, del_report_file

urlpatterns = [
	path('view_coprofiles', view_coprofiles, name = 'view_coprofiles'),
	path('add_coprofile', add_coprofile, name = 'add_coprofile'),
	path('del_coprofile/<int:pk>', del_coprofile, name = 'del_coprofile'),
	path('edit_coprofile/<int:pk>', edit_coprofile, name = 'edit_coprofile'),
	path('add_report_file/<int:pk>', add_report_file, name = 'add_report_file'),
	path('del_report_file/<int:pk>', del_report_file, name = 'del_report_file'),
]