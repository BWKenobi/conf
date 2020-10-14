import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileUdpateForm, EmailUdpateForm, ProfileUdpateFormFirst, UploadImageProfileForm
from ranty.forms import ChangePasswordForm
from .models import Profile
from companies.models import Staff, Company



@login_required(login_url='/login/')
def view_edit_profile(request):
	onboarding = request.user.profile.profile_onboarding
	if onboarding:
		request.user.profile.profile_onboarding=False
		request.user.profile.save()

	username = request.user.username

	if request.method=='POST':
		form_profile = ProfileUdpateForm(request.POST, instance=request.user.profile, label_suffix='')
		form_email= EmailUdpateForm(request.POST, instance=request.user, label_suffix='')
		form_password = ChangePasswordForm(request.POST, username=username)


		if form_profile.is_valid() and form_email.is_valid() and form_password.is_valid():
			if form_profile.has_changed():
				profile_form = form_profile.save(False)
				profile_form.save()	

			if form_email.has_changed():
				email = form_email.cleaned_data['email']
				request.user.profile.username = email
				request.user.profile.save()

				request.user.username = email
				request.user.email = email
				request.user.save()

			if form_password.cleaned_data['oldpassword'] and form_password.cleaned_data['newpassword']:
				user = request.user
				user.set_password(form_password.cleaned_data['newpassword'])
				user.save()
				update_session_auth_hash(request, user)

			if 'file' in request.FILES:
				request.user.profile.photo = request.FILES['file']
				request.user.profile.save()


			return redirect('profiles:view_edit_profile')

		args ={
			'onboarding': onboarding, 
			'form': form_profile, 
			'email': form_email, 
			'password': form_password
		}
		return render(request, 'profileuser/view_edit_profile.html', args)

	form_profile = ProfileUdpateForm(instance=request.user.profile, label_suffix='')
	form_email= EmailUdpateForm(instance=request.user, label_suffix='')
	form_password = ChangePasswordForm(username=username)
	form_image = UploadImageProfileForm()

	args = {
		'onboarding': onboarding, 
		'form': form_profile, 
		'email': form_email, 
		'password': form_password, 
		'image': form_image
	}
	return render(request, 'profileuser/view_edit_profile.html', args)


@login_required(login_url='/login/')
def view_user(request, pk):
	profile = Profile.objects.get(user_id=pk)
	my_staffs = Staff.objects.filter(employee=profile.user)
	companies = Company.objects.filter(staff__in=my_staffs, history_flag=False)

	args = {
		'profile': profile, 
		'companies': companies
	}
	return render(request, 'profileuser/view_user.html', args)



