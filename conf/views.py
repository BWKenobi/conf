import os
import time
from django.db.models import Q
from datetime import date
import json
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Mm, Pt

from fpdf import FPDF

from django.conf import settings
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import default_storage

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from .tokens import accaunt_activation_token

from profileuser.models import Profile
from coprofile.models import CoProfile
from .forms import UserLoginForm, UserRegistrationForm, ChangePasswordForm, CustomPasswordResetForm, CustomSetPasswordForm
from certificates.forms import MakeCertificateForm

class PDF(FPDF):
	pass

def home_view(request):
	dte = date.today()
	dte_deadline = date(2023,3,23)
	register_flag = False
	if dte<dte_deadline:
		register_flag = True

	args = {
		'register_flag': register_flag
	}
	return render(request, 'index.html', args)


def policy_view(request):
	return render(request, 'policy.html')


@login_required(login_url='/login/')
def admining_view(request):
	if not request.user.profile.message_accecc:
		return redirect('home')

	members = []
	form = MakeCertificateForm(label_suffix='')

	users = Profile.objects.all().exclude(username='admin').exclude(user__is_active=False). \
		order_by('-moderator_access', '-admin_access', '-speaker', 'surname', 'name', 'name2')

	for user in users:
		member = {
			'name': user.get_full_name(),
			'email': user.user.email,
			'status': user.get_speaker_display(),
			'work_place': user.work_place,
			'position': user.position,
			'cert': user.certificate_file,
			'cert_num': user.certificate_num,
		}
		members.append(member)
		comembers = CoProfile.objects.filter(lead=user.user)
		if comembers:
			for comember in comembers:
				member = {
					'name': comember.get_full_name(),
					'email': user.user.email,
					'status': comember.get_speaker_display(),
					'work_place': comember.work_place,
					'position': comember.position,
					'cert': comember.certificate_file,
					'cert_num': comember.certificate_num,
				}
				members.append(member)
	
	members =  sorted(members, key=lambda i: (i['name']))


	if request.POST:
		dte = date.today()
		document = Document()
		section = document.sections[-1]
		new_width, new_height = section.page_height, section.page_width
		section.orientation = WD_ORIENT.LANDSCAPE
		section.page_width = Mm(297)
		section.page_height = Mm(210)
		section.left_margin = Mm(30)
		section.right_margin = Mm(10)
		section.top_margin = Mm(10)
		section.bottom_margin = Mm(10)
		section.header_distance = Mm(10)
		section.footer_distance = Mm(10)

		style = document.styles['Normal']
		font = style.font
		font.name = 'Times New Roman'
		font.size = Pt(12)


		document.add_paragraph('Список участников/докладчиков семинара').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		p = document.add_paragraph()
		p.add_run(dte.strftime('%d.%b.%Y')).italic = True
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

		table = document.add_table(rows=1, cols=5)
		table.allow_autifit = False
		table.style = 'TableGrid'
		table.columns[0].width = Mm(10)
		table.columns[1].width = Mm(70)
		table.columns[2].width = Mm(30)
		table.columns[3].width = Mm(120)
		table.columns[4].width = Mm(27)

		hdr_cells = table.rows[0].cells
		hdr_cells[0].text = '№'
		hdr_cells[0].paragraphs[0].runs[0].font.bold = True
		hdr_cells[0].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		hdr_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
		hdr_cells[0].width = Mm(10)

		hdr_cells[1].text = 'ФИО/E-mail'
		hdr_cells[1].paragraphs[0].runs[0].font.bold = True
		hdr_cells[1].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		hdr_cells[1].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
		hdr_cells[1].width = Mm(70)

		hdr_cells[2].text = 'Статус'
		hdr_cells[2].paragraphs[0].runs[0].font.bold = True
		hdr_cells[2].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		hdr_cells[2].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
		hdr_cells[2].width = Mm(30)

		hdr_cells[3].text = 'Учреждение/должность'
		hdr_cells[3].paragraphs[0].runs[0].font.bold = True
		hdr_cells[3].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		hdr_cells[3].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
		hdr_cells[3].width = Mm(120)

		hdr_cells[4].text = 'Серт. №'
		hdr_cells[4].paragraphs[0].runs[0].font.bold = True
		hdr_cells[4].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		hdr_cells[4].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
		hdr_cells[4].width = Mm(27)

		count = 1

		for member in members:
			row_cells = table.add_row().cells
			row_cells[0].text = str(count)
			row_cells[0].paragraphs[0].runs[0].font.bold = True
			row_cells[0].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
			row_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
			row_cells[0].width = Mm(10)

			row_cells[1].text = member['name'] + '\n' + member['email']
			row_cells[1].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
			row_cells[1].width = Mm(70)

			row_cells[2].text = member['status']
			row_cells[2].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
			row_cells[2].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
			row_cells[2].width = Mm(30)

			row_cells[3].text = member['work_place'] + '\n' + member['position']
			row_cells[3].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
			row_cells[3].width = Mm(120)

			row_cells[4].text = member['cert_num']
			row_cells[4].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
			row_cells[4].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
			row_cells[4].width = Mm(27)

			count += 1



		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
		response['Content-Disposition'] = 'attachment; filename=List (' + dte.strftime('%d-%b-%Y') + ').docx'
		document.save(response)

		return response

	args = {
		'menu': 'admining',
		'users': users,
		'members': members,
		'form': form
	}
	return render(request, 'admining.html', args)


def login_view(request):
	form = UserLoginForm(request.POST or None)
	next_ = request.GET.get('next')
	modal = False

	if form.is_valid():
		username = request.POST.get('email').lower()
		password = request.POST.get('password')
		user = authenticate(username = username.strip(), password = password.strip())
		
		login(request, user)
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or '/'


		return redirect(redirect_path)

	args = {
		'form': form
	}
	return render(request, 'login.html', args)


def logout_view(request):
	logout(request)
	return redirect('home')


def register_view(request):
	if request.method=='POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.username = new_user.email
			new_user.is_active = False
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()

			new_user.profile.name = user_form.cleaned_data['name']
			new_user.profile.name2 = user_form.cleaned_data['name2']
			new_user.profile.surname = user_form.cleaned_data['surname']
			new_user.profile.work_place = user_form.cleaned_data['work_place']

			new_user.profile.position = user_form.cleaned_data['position']
			new_user.profile.speaker = user_form.cleaned_data['speaker']
			new_user.profile.save()


			current_site = get_current_site(request)
			protocol = 'http'
			if request.is_secure():
				protocol = 'https'

			mail_subject = 'Активация аккаунта'
			to_email = new_user.email
			#if '127.0.0.1' in current_site.domain:
			uid = urlsafe_base64_encode(force_bytes(new_user.pk))
			#else:
			#	uid = urlsafe_base64_encode(force_bytes(new_user.pk)).decode()

			token = accaunt_activation_token.make_token(new_user)

			message = render_to_string('acc_active_email.html', {'user': new_user, 'domain': current_site.domain,\
				'uid': uid, \
				'token': token,\
				'protocol': protocol,\
				'email': to_email})

			message_html = render_to_string('acc_active_email_html.html', {'user': new_user, 'domain': current_site.domain,\
				'uid': uid, \
				'token': token,\
				'protocol': protocol,\
				'email': to_email})

			t = send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=True, html_message=message_html)

			return render(request, 'confirm_email.html')

		return render(request, 'register.html', {'form': user_form})

	user_form = UserRegistrationForm()
	return render(request, 'register.html', {'form': user_form})


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user and accaunt_activation_token.check_token(user, token):
		user.is_active = True
		user.save()

		login(request, user)
		return redirect('home')

	return render(request, 'failed_email.html')


def change_password(request):
	username = request.user.username

	if request.method == 'POST':
		form = ChangePasswordForm(request.POST, username=username)

		if form.is_valid():
			user = request.user
			user.set_password(form.cleaned_data['newpassword1'])
			user.save()
			update_session_auth_hash(request, user)

			return redirect('profiles:view_edit_profile')

		args = {
			'form': form
		}
		return render(request, 'change_password.html', args)

	form = ChangePasswordForm(username=username)

	args = {
		'form': form
	}
	return render(request, 'change_password.html', args)


# --------------------------------
#           Для ajax'а
# --------------------------------
def change_admin_access(request):
	user_id = request.GET.get('user_id')
	access = request.GET.get('access')
	if access=='true':
		access = True
	else:
		access = False
	
	profile = Profile.objects.get(id = user_id)
	profile.admin_access = access
	profile.save()
	
	return HttpResponse(json.dumps('Статус изменен.'))


def change_moderate_access(request):
	user_id = request.GET.get('user_id')
	access = request.GET.get('access')
	if access=='true':
		access = True
	else:
		access = False
	
	profile = Profile.objects.get(id = user_id)
	profile.moderator_access = access
	profile.save()
	
	return HttpResponse(json.dumps('Статус изменен.'))


def send_info_message(request):
	users = User.objects.all().exclude(username='admin').exclude(is_active=False)
	count = 0

	for user in users:
		mail_subject = 'Информационное письмо'
		to_email = user.email
		sex = user.profile.sex()
		sex_valid = user.profile.sex_valid()
		
		message = render_to_string('info_email.html', {'sex_valid': sex_valid, 'sex': sex, 'name': user.profile.get_io_name()})

		message_html = render_to_string('info_email_html.html', {'sex_valid': sex_valid, 'sex': sex, 'name': user.profile.get_io_name()})

		email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])

		docfile = default_storage.open(user.profile.certificate_file.name, 'r')

		email.attach_file(docfile.name)

		email.send()

		#send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=True, html_message=message_html)

		count += 1

		if count==5:
			count = 0
			time.sleep(1.5)

		cousers = CoProfile.objects.filter(lead=user)
		if cousers:
			for couser in cousers:
				mail_subject = 'Информационное письмо'
				to_email = user.email
				sex = couser.sex()
				sex_valid = couser.sex_valid()
				
				message = render_to_string('info_email.html', {'sex_valid': sex_valid, 'sex': sex, 'name': couser.get_io_name()})

				message_html = render_to_string('info_email_html.html', {'sex_valid': sex_valid, 'sex': sex, 'name': couser.get_io_name()})

				email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])

				docfile = default_storage.open(couser.certificate_file.name, 'r')

				email.attach_file(docfile.name)

				email.send()

				#send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=True, html_message=message_html)

				count += 1

				if count==5:
					count = 0
					time.sleep(1.5)

	return HttpResponse(json.dumps('Сообщения разосланы.'))