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
from .forms import UserLoginForm, UserRegistrationForm, ChangePasswordForm, CustomPasswordResetForm, CustomSetPasswordForm

class PDF(FPDF):
	pass

def home_view(request):

	users = Profile.objects.all().exclude(username='admin').exclude(user__is_active=False). \
		order_by('-moderator_access', '-admin_access', '-speaker', 'surname', 'name', 'name2')

	speakers = Profile.objects.filter(speaker=True).exclude(username='admin'). \
		order_by('surname', 'name', 'name2')

	if request.POST:
		dte = date.today()
		document = Document()
		section = document.sections[-1]
		new_width, new_height = section.page_height, section.page_width
		section.orientation = WD_ORIENT.PORTRAIT
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


		document.add_paragraph('Список участников конференции').paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
		p = document.add_paragraph()
		p.add_run(dte.strftime('%d.%b.%Y')).italic = True
		p.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT

		table = document.add_table(rows=1, cols=6)
		table.allow_autifit = False
		table.style = 'TableGrid'
		table.columns[0].width = Mm(10)
		table.columns[1].width = Mm(70)
		table.columns[2].width = Mm(70)
		table.columns[3].width = Mm(60)
		table.columns[4].width = Mm(25)
		table.columns[5].width = Mm(22)

		hdr_cells = table.rows[0].cells
		hdr_cells[0].text = '№'
		hdr_cells[0].width = Mm(10)
		hdr_cells[1].text = 'ФИО'
		hdr_cells[1].width = Mm(70)
		hdr_cells[2].text = 'Место работы'
		hdr_cells[2].width = Mm(70)
		hdr_cells[3].text = 'E-mail'
		hdr_cells[3].width = Mm(60)
		hdr_cells[4].text = 'Статус'
		hdr_cells[4].width = Mm(25)
		hdr_cells[5].text = 'Серт. №'
		hdr_cells[5].width = Mm(22)

		count = 1

		users_sorted = users.order_by('surname', 'name', 'name2')
		for usr in users_sorted:
			row_cells = table.add_row().cells
			row_cells[0].text = str(count)
			row_cells[0].width = Mm(10)
			row_cells[1].text = usr.get_full_name()
			row_cells[1].width = Mm(70)
			row_cells[2].text = usr.work_place
			row_cells[2].width = Mm(70)
			row_cells[3].text = usr.user.email
			row_cells[3].width = Mm(60)
			if usr.speaker:
				row_cells[4].text = 'Докладчик'
			else:
				row_cells[4].text = 'Участник'
			row_cells[4].width = Mm(25)
			row_cells[5].text = usr.certificate_num
			row_cells[5].width = Mm(22)
			count += 1



		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
		response['Content-Disposition'] = 'attachment; filename=List (' + dte.strftime('%d-%b-%Y') + ').docx'
		#document.save(response)
		document.save(os.path.join(settings.MEDIA_ROOT, '111.docx'))

		return response

	dte = date.today()
	dte_deadline = date(2020,10,29)
	register_flag = False
	if dte<dte_deadline:
		register_flag = True

	args = {
		'users': users,
		'speakers': speakers,
		'register_flag': register_flag
	}
	return render(request, 'index.html', args)


def policy_view(request):
	return render(request, 'policy.html')


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
			new_user.profile.save()


			current_site = get_current_site(request)
			protocol = 'http'
			if request.is_secure():
				protocol = 'https'

			mail_subject = 'Активация аккаунта'
			to_email = new_user.email
			if '127.0.0.1' in current_site.domain:
				uid = urlsafe_base64_encode(force_bytes(new_user.pk))
			else:
				uid = urlsafe_base64_encode(force_bytes(new_user.pk)).decode()

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

			send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=True, html_message=message_html)

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
		
		message = render_to_string('info_email.html', {'sex': sex, 'name': user.profile.get_io_name()})

		message_html = render_to_string('info_email_html.html', {'sex': sex, 'name': user.profile.get_io_name()})

		email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])

		docfile = default_storage.open(user.profile.certificate_file.name, 'r')

		email.attach_file(docfile.name)

		email.send()

		#send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=True, html_message=message_html)

		count += 1

		if count==5:
			count = 0
			time.sleep(1.5)

	return HttpResponse(json.dumps('Сообщения разосланы.'))