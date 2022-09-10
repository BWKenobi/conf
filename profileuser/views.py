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

from .forms import ProfileUdpateForm, ProfileAddReprotForm

from .models import Profile


@login_required(login_url='/login/')
def view_edit_profile(request):
	username = request.user.username

	dte = date.today()
	dte_deadline = date(2022,10,28)
	report_flag = False
	if dte<dte_deadline:
		report_flag = True


	if request.method=='POST':
		form_profile = ProfileUdpateForm(request.POST, instance=request.user.profile, label_suffix='')

		if "passchange" in request.POST:
			return redirect('passchange')

		if 'addfile' in request.POST:
			return redirect('profiles:add_report_file')

		if form_profile.is_valid():
			if form_profile.has_changed():
				profile_form = form_profile.save(False)
				profile_form.save()	

			
			return redirect('home')

		args ={
			'report_flag': report_flag,
			'form': form_profile, 
		}
		return render(request, 'profileuser/view_edit_profile.html', args)

	form_profile = ProfileUdpateForm(instance=request.user.profile, label_suffix='')

	args = {
		'report_flag': report_flag,
		'form': form_profile, 
	}
	return render(request, 'profileuser/view_edit_profile.html', args)


@login_required(login_url='/login/')
def add_report_file(request):
	if request.method=='POST':
		form = ProfileAddReprotForm(request.POST, request.FILES, instance=request.user.profile, label_suffix='')

		if form.is_valid():
			profile_form = form.save(False)
			profile_form.speaker = True
			profile_form.save()	


			speaker = request.user.profile

			mail_subject = 'Новый доклад конференции'
			moderators = Profile.objects.filter(moderator_access=True)
			e_mails = []
			for moderator in moderators:
				e_mails.append(moderator.user.email)

			if e_mails:
				message = render_to_string('profileuser/speaker_email.html', {'speaker': speaker})
				message_html = render_to_string('profileuser/speaker_email_html.html', {'speaker': speaker})

				#send_mail(mail_subject, message, settings.EMAIL_HOST_USER, e_mails, fail_silently=True, html_message=message_html)

				email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, e_mails)

				docfile = default_storage.open(speaker.report_file.name, 'r')

				email.attach_file(docfile.name)

				email.send()
			
			return redirect('profiles:view_edit_profile')

		args = {
			'form': form
		}
		return render(request, 'profileuser/add_report_file.html', args)

	form = ProfileAddReprotForm()

	args = {
		'form': form
	}
	return render(request, 'profileuser/add_report_file.html', args)