import os
import datetime

from datetime import date
from django.http import HttpResponse

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from django.contrib.auth.models import User

from .forms import ProfileUdpateForm, ProfileAddReprotForm, ProfileAddReprotFileForm
from conf.forms import SectionForm

from .models import Profile
from sections.models import Section

@login_required(login_url='/login/')
def view_edit_profile(request):
	username = request.user.username
	user = request.user

	dte = date.today()
	dte_deadline = date(2024,10,14)
	report_flag = False
	if dte<dte_deadline:
		report_flag = True

	modal = False

	form_profile = ProfileUdpateForm(instance=request.user.profile, label_suffix='')

	if request.method=='POST':
		form_profile = ProfileUdpateForm(request.POST, instance=request.user.profile, label_suffix='')

		if "passchange" in request.POST:
			return redirect('passchange')

		if 'addfile' in request.POST:
			return redirect('profiles:add_report_file')

		if form_profile.is_valid():
			profile_form = form_profile.save(False)
			profile_form.save()	

			if profile_form.speaker == '3':
				profile_form.report_name = ''
				profile_form.report_file = None
				profile_form.save()

			modal = True

	args = {
		'menu': 'profile',
		'user': user,
		'report_flag': report_flag,
		'form': form_profile, 
		'modal': modal
	}
	return render(request, 'profileuser/view_edit_profile.html', args)


@login_required(login_url='/login/')
def add_report_file(request):
	user = request.user
	edit = False
	if user.profile.report_file:
		edit = True

	if request.method=='POST':
		form = ProfileAddReprotForm(request.POST, instance=request.user.profile, label_suffix='')
		file = ProfileAddReprotFileForm(request.POST, request.FILES, edit = edit)

		if form.is_valid() and file.is_valid():
			profile_form = form.save(False)
			if 'report_file' in request.FILES:
				profile_form.report_file = request.FILES['report_file']

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

				if speaker.report_file:
					docfile = default_storage.open(speaker.report_file.name, 'r')

					email.attach_file(docfile.name)

				email.send()
			
			return redirect('profiles:view_edit_profile')

		args = {
			'menu': 'profile',
			'form': form,
			'file': file,
			'user': user,
		}
		return render(request, 'profileuser/add_report_file.html', args)

	form = ProfileAddReprotForm(instance=request.user.profile)
	file = ProfileAddReprotFileForm(edit = edit)

	args = {
		'menu': 'profile',
		'form': form,
		'file': file,
		'user': user
	}
	return render(request, 'profileuser/add_report_file.html', args)


@login_required(login_url='/login/')
def del_report_file(request):
	user = request.user

	if user.profile.report_name:
		user.profile.report_file = None
		user.profile.report_name = ''
		user.profile.save()


	return redirect('profiles:view_edit_profile')


@login_required(login_url='/login/')
def unregistered(request):
	members = Profile.objects.all().exclude(username='admin'). \
		order_by('surname', 'name', 'name2')

	args = {
		'menu': 'unregistered',
		'members': members,
	}
	return render(request, 'profileuser/unregistered.html', args)


@login_required(login_url='/login/')
def set_section(request):
	user = request.user
	pk = request.GET['pk']
	section = Section.objects.filter(pk = pk).first()
	if not section:
		return HttpResponse('0')

	user.profile.section = section
	user.profile.save()

	user_count = User.objects.filter(profile__section = section, is_active = True).count()
	if user_count <= section.count:
		return HttpResponse('1')

	user.profile.section = None
	user.profile.save()

	section_form = SectionForm(label_suffix='')

	return HttpResponse(render_to_string('profileuser/section_form.html', {'section_form': section_form}))


@login_required(login_url='/login/')
def acivate(request):
	pk = request.GET['pk']
	profile = Profile.objects.filter(pk = pk).first()

	if not profile:
		return HttpResponse(False)

	profile.user.is_active = True
	profile.user.save()

	user_count = User.objects.filter(profile__section = profile.section, is_active = True).count()
	if profile.section:
		if user_count > profile.section.count:
			profile.section = None
			profile.save()

	return HttpResponse(True)


@login_required(login_url='/login/')
def deactivate(request):
	pk = request.GET['pk']
	profile = Profile.objects.filter(pk = pk).first()

	if not profile:
		return HttpResponse(False)

	profile.user.is_active = False
	profile.user.save()

	return HttpResponse(True)