import os
import io
import time
from datetime import date
import json
from io import BytesIO
import base64

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile

from pytils import translit

from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from zipfile import ZipFile

from fpdf import FPDF

from profileuser.models import Profile
from coprofile.models import CoProfile


class PDF(FPDF):
	pass


def del_serificates(request):
	users = Profile.objects.all().exclude(username='admin').exclude(user__is_active=False)

	for user in users:
		user.certificate_num = ''
		user.certificate_file = None
		user.save()
		comembers = CoProfile.objects.filter(lead=user.user)
		for comember in comembers:
			comember.certificate_num = ''
			comember.certificate_file = None
			comember.save()

	return redirect('home')



def send_serificates(request):
	users = Profile.objects.all().exclude(username='admin').exclude(user__is_active=False)
	
	signature = 'С уважением,\r\nавторы портала - AstVisionScience'
	sign = signature.split('\r\n')
	message = 'Во вложении иенные сертификаты'
	text = message.split('\r\n')

	count = 0
	for user in users:
		mail_subject = 'Информационное письмо'
		to_email = user.user.email
		sex = user.sex()
		sex_valid = user.sex_valid()
		name = user.get_io_name()

		args = {
			'sex_valid': sex_valid,
			'sex': sex, 
			'name': name,
			'message': message,
			'text': text,
			'signature': signature,
			'sign': sign
		}
		
		message = render_to_string('info_email.html', args)

		message_html = render_to_string('info_email_html.html', args)

		email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])

		email.attach_file(user.certificate_file.path)
		
		comembers = CoProfile.objects.filter(lead=user.user)
		for comember in comembers:
			email.attach_file(comember.certificate_file.path)


		
		email.send()

		#send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=True, html_message=message_html)

		count += 1

		if count==5:
			count = 0
			time.sleep(1.5)




	return redirect('home')


def generate_sertificates(request):
	sertificate_num = int(request.GET['field1'])
	sertificate_add = request.GET['field2']
	if not sertificate_add:
		sertificate_add = ' '
	sertificate_add += request.GET['field3']


	members = []

	users = Profile.objects.all().exclude(username='admin').exclude(user__is_active=False). \
		order_by('-moderator_access', '-admin_access', '-speaker', 'surname', 'name', 'name2')

	for user in users:
		member = {
			'name': user.get_full_name(),
			'status': user.speaker,
			'model': user
		}
		members.append(member)
		comembers = CoProfile.objects.filter(lead=user.user)
		if comembers:
			for comember in comembers:
				member = {
					'name': comember.get_full_name(),
					'status': comember.speaker,
					'model': comember
				}
				members.append(member)
	
	members =  sorted(members, key=lambda i: (i['name']))

	time.sleep(1)

	
	font_url = os.path.join(settings.BASE_DIR, 'static/fonts/chekhovskoy.ttf')
	img_speaker_url = os.path.join(settings.BASE_DIR, 'static/img/sertificate_speaker.jpg')
	img_member_url = os.path.join(settings.BASE_DIR, 'static/img/sertificate_member.jpg')

	for member in members:
		sertificate_str_num = str(sertificate_num)+sertificate_add
		pdf = PDF(orientation='L', unit='mm', format='A4')
		pdf.add_page()
		pdf.add_font('Chehkovskoy', '', font_url , uni=True)
		
		if member['status']!='3':
			pdf.image(img_speaker_url, 0, 0, pdf.w, pdf.h)
		else:
			pdf.image(img_member_url, 0, 0, pdf.w, pdf.h)
		
		pdf.set_font('Chehkovskoy', '', 18)
		pdf.set_text_color(0, 0, 0)
		pdf.set_xy(0.0, 110.0)
		pdf.cell(w=297.0, h=5.0, align='C', txt = '№' + sertificate_str_num)
		pdf.set_xy(0.0, 130.0)
		pdf.cell(w=297.0, h=5.0, align='C', txt = member['name'])

		pdf.output(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), 'F')
		file  = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), 'rb')
		djangofile = File(file)

		member['model'].certificate_file.save((member['name'])+'.pdf', djangofile)
		member['model'].certificate_num = sertificate_str_num
		member['model'].save()

		file.close()

		sertificate_num += 1
	sertificate_num -= 1

	return HttpResponse(json.dumps({'last_num': str(sertificate_num) + sertificate_add}))

