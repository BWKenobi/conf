from django.urls import path
from django.conf.urls import url
from .views import view_edit_profile, add_report_file, del_report_file

urlpatterns = [
	path('view_edit_profile', view_edit_profile, name = 'view_edit_profile'),
	path('add_report_file', add_report_file, name = 'add_report_file'),
	path('del_report_file', del_report_file, name = 'del_report_file'),
]