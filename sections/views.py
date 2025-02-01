import os
import datetime
import time

from datetime import date

from django.conf import settings
from django.core.files.storage import default_storage

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from .models import Section
from .forms import SectionForm


@login_required(login_url='/login/')
def sections(request):
	if not request.user.profile.admin_access:
		return redirect('home')
		
	sections = Section.objects.all().order_by('name')

	args = {
		'menu': 'sections',
		'sections': sections,
	}
	return render(request, 'sections/sections.html', args)


@login_required(login_url='/login/')
def add_section(request):
	if not request.user.profile.admin_access:
		return redirect('home')

	if request.method=='POST':
		form = SectionForm(request.POST, label_suffix='')
		if form.is_valid():
			new_section = form.save(False)
			new_section.save()

			return redirect('sections:sections')
			
		args = {
			'menu': 'sections',
			'form': form
		}
		return render(request, 'sections/add_section.html', args)

	form = SectionForm(label_suffix='')
	args = {
		'menu': 'sections',
		'form': form
	}
	return render(request, 'sections/add_section.html', args)


@login_required(login_url='/login/')
def edit_section(request, pk):
	if not request.user.profile.admin_access:
		return redirect('home')

	section = Section.objects.filter(pk = pk).first()
	if not section:
		return redirect('sections:sections')

	if request.method=='POST':
		form = SectionForm(request.POST, instance=section, label_suffix='')

		if form.is_valid():
			section_form = form.save(False)
			section_form.save()	

			return redirect('sections:sections')

		args = {
			'menu': 'sections',
			'section': section,
			'form': form,
		}
		return render(request, 'sections/edit_section.html', args)


	form = SectionForm(instance=section, label_suffix='')

	args = {
		'menu': 'sections',
		'section': section,
		'form': form,
	}
	return render(request, 'sections/edit_section.html', args)