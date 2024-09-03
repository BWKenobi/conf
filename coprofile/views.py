import os
import datetime

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from .forms import CoProfileUdpateForm, CoProfileAddReprotForm, CoProfileAddReprotFileForm, CoProfileRegistrationForm

from .models import CoProfile
from profileuser.models import Profile


@login_required(login_url='/login/')
def view_coprofiles(request):
	user = request.user
	
	dte = date.today()
	dte_deadline = date(2022,10,28)
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
				phone = user_form.cleaned_data['phone'],
				work_part = user_form.cleaned_data['work_part'],
				position = user_form.cleaned_data['position'],
				degree = user_form.cleaned_data['degree'],
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

	dte = date.today()
	dte_deadline = date(2024,10,14)
	report_flag = False
	if dte<dte_deadline:
		report_flag = True

	modal = False
	form_profile = CoProfileUdpateForm(instance=coprofile)

	if request.method=='POST':
		form_profile = CoProfileUdpateForm(request.POST, instance=coprofile)

		if 'addfile' in request.POST:
			return redirect('coprofile:add_report_file', pk=coprofile.pk)

		if form_profile.is_valid():
			profile_form = form_profile.save(False)
			profile_form.save()	

			if profile_form.speaker == '3':
				profile_form.report_name = ''
				profile_form.report_file = None
				profile_form.save()

			modal = True


	args = {
		'menu': 'coprofile',
		'coprofile': coprofile,
		'report_flag': report_flag,
		'form': form_profile,
		'modal': modal
	}
	return render(request, 'coprofile/edit_coprofile.html', args)



@login_required(login_url='/login/')
def add_report_file(request, pk):
	coprofile = CoProfile.objects.get(pk = pk)
	edit = False
	if coprofile.report_file:
		edit = True

	if request.method=='POST':
		form = CoProfileAddReprotForm(request.POST, instance=coprofile)
		file = CoProfileAddReprotFileForm(request.POST, request.FILES, edit = edit)

		if form.is_valid() and file.is_valid():
			profile_form = form.save(False)
			if 'report_file' in request.FILES:
				profile_form.report_file = request.FILES['report_file']

			profile_form.save()	

			speaker = coprofile

			mail_subject = 'Новый доклад конференции'
			moderators = Profile.objects.filter(moderator_access=True)
			e_mails = []
			for moderator in moderators:
				e_mails.append(moderator.user.email)

			if e_mails:
				message = render_to_string('coprofile/speaker_email.html', {'speaker': speaker})
				message_html = render_to_string('coprofile/speaker_email_html.html', {'speaker': speaker})

				#send_mail(mail_subject, message, settings.EMAIL_HOST_USER, e_mails, fail_silently=True, html_message=message_html)

				email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, e_mails)

				docfile = default_storage.open(speaker.report_file.name, 'r')

				email.attach_file(docfile.name)

				email.send()
			
			return redirect('coprofile:edit_coprofile', pk = coprofile.pk)

		args = {
			'menu': 'coprofile',
			'coprofile': coprofile,
			'form': form,
			'file': file
		}
		return render(request, 'coprofile/add_report_file.html', args)

	form = CoProfileAddReprotForm(instance=coprofile)
	file = CoProfileAddReprotFileForm(edit = edit)


	args = {
		'menu': 'coprofile',
		'coprofile': coprofile,
		'form': form,
		'file': file
	}
	return render(request, 'coprofile/add_report_file.html', args)