import os

from datetime import date
from datetime import time
from datetime import datetime

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from .forms import ProfileUdpateForm

from .models import Profile


@login_required(login_url='/login/')
def view_edit_profile(request):
	username = request.user.username

	dte = datetime.now()
	dte_deadline = datetime(2023,3,23,14,00)
	report_flag = False
	if dte<dte_deadline:
		report_flag = True


	if request.method=='POST':
		form_profile = ProfileUdpateForm(request.POST, instance=request.user.profile, label_suffix='')

		if "passchange" in request.POST:
			return redirect('passchange')

		if form_profile.is_valid():
			if form_profile.has_changed():
				profile_form = form_profile.save(False)
				profile_form.save()	

			
			return redirect('home')

		args ={
			'menu': 'profile',
			'report_flag': report_flag,
			'form': form_profile, 
		}
		return render(request, 'profileuser/view_edit_profile.html', args)

	form_profile = ProfileUdpateForm(instance=request.user.profile, label_suffix='')

	args = {
		'menu': 'profile',
		'report_flag': report_flag,
		'form': form_profile, 
	}
	return render(request, 'profileuser/view_edit_profile.html', args)

