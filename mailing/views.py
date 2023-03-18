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

from .forms import InfoMailForm


@login_required(login_url='/login/')
def send_info_message(request):
	if not request.user.profile.message_accecc:
		return redirect('home')
		
	signature = 'С уважением,\r\nавторы портала - НА-КАНКУРС.РФ'

	if request.method=='POST':
		form_message = InfoMailForm(request.POST, label_suffix='')

		if form_message.is_valid():
			if form_message.cleaned_data['signature']:
				signature = form_message.cleaned_data['signature']

			users = User.objects.all().exclude(username='admin').exclude(is_active=False)
			mail_subject = form_message.cleaned_data['theme']
			text = form_message.cleaned_data['msg'].split('\r\n')
			sign = signature.split('\r\n')

			count = 0
			for user in users:
				to_email = user.email
				sex = user.profile.sex()
				sex_valid = user.profile.sex_valid()

				args = {
					'sex': sex,
					'sex_valid': sex_valid,
					'name': user.profile.get_io_name(),
					'message': form_message.cleaned_data['msg'],
					'text': text,
					'signature': signature,
					'sign': sign
				}
				
				message = render_to_string('mailing/info_email.html', args)

				message_html = render_to_string('mailing/info_email_html.html', args)

				send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=True, html_message=message_html)

				count += 1

				if count==5:
					count = 0
					time.sleep(1.5)


	
			return redirect('home')


	form_message= InfoMailForm(label_suffix='')

	args = {
		'menu': 'mailing',
		'form': form_message, 
	}
	return render(request, 'mailing/send_info_message.html', args)