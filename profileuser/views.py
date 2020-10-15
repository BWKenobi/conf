import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import ProfileUdpateForm

from .models import Profile


@login_required(login_url='/login/')
def view_edit_profile(request):
	username = request.user.username

	if request.method=='POST':
		form_profile = ProfileUdpateForm(request.POST, instance=request.user.profile, label_suffix='')

		if "passchange" in request.POST:
			return redirect('passchange')

		if form_profile.is_valid():
			if form_profile.has_changed():
				profile_form = form_profile.save(False)
				profile_form.save()	

			
			return redirect('home')

		args ={
			'form': form_profile, 
		}
		return render(request, 'profileuser/view_edit_profile.html', args)

	form_profile = ProfileUdpateForm(instance=request.user.profile, label_suffix='')

	args = {
		'form': form_profile, 
	}
	return render(request, 'profileuser/view_edit_profile.html', args)


