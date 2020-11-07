import os
import time
from datetime import date
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile

from fpdf import FPDF

from profileuser.models import Profile


class PDF(FPDF):
	pass


def generate_sertificates(request):
	users = Profile.objects.all().exclude(username='admin').exclude(user__is_active=False). \
		order_by('surname', 'name', 'name2')

	
	font_url = os.path.join(settings.BASE_DIR, 'static/fonts/chekhovskoy.ttf')
	img_speaker_url = os.path.join(settings.BASE_DIR, 'static/img/sertificate_speaker.jpg')
	img_member_url = os.path.join(settings.BASE_DIR, 'static/img/sertificate_member.jpg')
	sertificate_num = 33

	for user in users:
		sertificate_str_num = str(sertificate_num)+'-20'
		pdf = PDF(orientation='L', unit='mm', format='A4')
		pdf.add_page()
		pdf.add_font('Chehkovskoy', '', font_url , uni=True)
		
#		if user.speaker:
#			pdf.image(img_speaker_url, 0, 0, pdf.w, pdf.h)
#		else:
#			pdf.image(img_member_url, 0, 0, pdf.w, pdf.h)
		
#		pdf.set_font('Chehkovskoy', '', 18)
#		pdf.set_text_color(0, 0, 0)
#		pdf.set_xy(0.0, 110.0)
#		pdf.cell(w=297.0, h=5.0, align='C', txt = '№' + sertificate_str_num)
#		pdf.set_xy(0.0, 130.0)
#		pdf.cell(w=297.0, h=5.0, align='C', txt = user.get_full_name())
#		pdf.output('test.pdf', 'F')
#		file  = open('test.pdf', 'rb')
#		djangofile = File(file)

#		user.certificate_file.save((user.get_file_name())+'.pdf', djangofile)
#		user.certificate_num = sertificate_str_num
#		user.save()

#		file.close()

#		sertificate_num += 1
#	sertificate_num -= 1

#	return HttpResponse(json.dumps({'last_num': str(sertificate_num) + '-20'}))

	return HttpResponse(json.dumps("1111"))
