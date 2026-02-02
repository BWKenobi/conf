from datetime import date
from django.contrib.sites.shortcuts import get_current_site


def base_context(request):
	dte = date.today()
	dte_deadline = date(2026,2,25)
	dte_zoom = date(2026,2,26)

	register_flag = False
	if dte<dte_deadline:
		register_flag = True

	zoom_flag = False
	if dte>=dte_zoom:
		zoom_flag = True

	cookie_flag = True
	if "coockes" in request.session:
		cookie_flag = False
		if request.user.is_authenticated:
			if request.session['coockes'] == '1' and not request.user.profile.cookies_agree:
				request.user.profile.cookies_agree = True
				request.user.profile.save()

	else:
		if request.user.is_authenticated:
			if request.user.profile.cookies_agree:
				cookie_flag = False

	args = {
		'register_flag': register_flag,
		'zoom_flag': zoom_flag,
		'cookie_flag': cookie_flag
	}
	return args
