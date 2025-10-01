from datetime import date
from django.contrib.sites.shortcuts import get_current_site


def base_context(request):
	dte = date.today()
	dte_deadline = date(2025,10,8)
	dte_zoom = date(2024,10,22)

	register_flag = False
	if dte<dte_deadline:
		register_flag = True

	zoom_flag = False
	if dte>=dte_zoom:
		zoom_flag = True

	args = {
		'register_flag': register_flag,
		'zoom_flag': zoom_flag,
	}
	return args
