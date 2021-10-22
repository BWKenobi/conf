import os
import time
from datetime import date
import json
from io import BytesIO
import base64

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile

from fpdf import FPDF

from profileuser.models import Profile
from coprofile.models import CoProfile


class PDF(FPDF):
	pass


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
			'status': user.status(),
			'model': user
		}
		members.append(member)
		comembers = CoProfile.objects.filter(lead=user.user)
		if comembers:
			for comember in comembers:
				member = {
					'name': comember.get_full_name(),
					'status': comember.status(),
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
		
		if member['status']=='Докладчик':
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

