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

from .forms import CoProfileUdpateForm, CoProfileRegistrationForm

from .models import CoProfile
from profileuser.models import Profile


@login_required(login_url='/login/')
def view_coprofiles(request):
	user = request.user
	
	dte = datetime.now()
	dte_deadline = datetime(2023,3,23,14,00)
	report_flag = False
	if dte<dte_deadline:
		report_flag = True

	coprofiles = CoProfile.objects.filter(lead = user)

	args = {
		'menu': 'coprofile',
		'report_flag': report_flag,
		'coprofiles': coprofiles,
	}
	return render(request, 'coprofile/view_coprofiles.html', args)


@login_required(login_url='/login/')
def add_coprofile(request):
	user = request.user

	if request.method=='POST':
		user_form = CoProfileRegistrationForm(request.POST)
		if user_form.is_valid():
			CoProfile.objects.create(
				lead = user,
				name = user_form.cleaned_data['name'],
				name2 = user_form.cleaned_data['name2'],
				surname = user_form.cleaned_data['surname'],
				work_place = user_form.cleaned_data['work_place'],
				position = user_form.cleaned_data['position'],
				speaker = user_form.cleaned_data['speaker']
			)

			return redirect('coprofile:view_coprofiles')
			
		args = {
			'menu': 'coprofile',
			'form': user_form
		}
		return render(request, 'coprofile/add_coprofile.html', args)

	user_form = CoProfileRegistrationForm()
	args = {
		'menu': 'coprofile',
		'form': user_form
	}
	return render(request, 'coprofile/add_coprofile.html', args)



@login_required(login_url='/login/')
def del_coprofile(request, pk):
	user = request.user

	coprofile = CoProfile.objects.get(pk = pk)
	coprofile.delete()
	return redirect('coprofile:view_coprofiles')


@login_required(login_url='/login/')
def edit_coprofile(request, pk):
	coprofile = CoProfile.objects.get(pk = pk)

	dte = datetime.now()
	dte_deadline = datetime(2023,3,23,14,00)
	report_flag = False
	if dte<dte_deadline:
		report_flag = True

	if request.method=='POST':
		form_profile = CoProfileUdpateForm(request.POST, instance=coprofile, label_suffix='')

		if 'addfile' in request.POST:
			return redirect('coprofile:add_report_file', pk=coprofile.pk)

		if form_profile.is_valid():
			if form_profile.has_changed():
				profile_form = form_profile.save(False)
				profile_form.save()	

			
			return redirect('coprofile:view_coprofiles')

		args = {
			'menu': 'coprofile',
			'coprofile': coprofile,
			'report_flag': report_flag,
			'form': form_profile,
		}
		return render(request, 'coprofile/edit_coprofile.html', args)




	form_profile = CoProfileUdpateForm(instance=coprofile, label_suffix='')

	args = {
		'menu': 'coprofile',
		'coprofile': coprofile,
		'report_flag': report_flag,
		'form': form_profile,
	}
	return render(request, 'coprofile/edit_coprofile.html', args)

