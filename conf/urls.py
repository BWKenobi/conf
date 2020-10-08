from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.urls import include
from django.contrib.auth import views as auth_views

from . views import home_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name = 'home'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


#urlpatterns += [
#    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(form_class = CustomPasswordResetForm), name = 'password_reset'),
#    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
#    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm), name = 'password_reset_confirm'),
#    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_comlete.html'), name = 'password_reset_complete'),
#    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name = 'activate'),
#]
