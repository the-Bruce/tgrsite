from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	
	url(r'^user/edit/', views.edit, name='edit'),

	url(r'^user/(?P<pk>[0-9]+)/$', views.viewmember, name='user'),
	url(r'^user/me/$', views.viewmember, {'pk': 'me'}, name='me'),

	url(r'^user/update/$', views.update, name='update'),

	url(r'^user/allmembers/$', views.allmembers, name='allmembers'),

	# TODO: Reimplement auth stuff using Django built-in auth views
	# https://docs.djangoproject.com/en/1.11/topics/auth/default/#built-in-auth-views
	url(r'^login/done/', views.login_process, name='login-done'),
	url(r'^login/', views.login_view, name='login'),

	url(r'^signup/done', views.signup_process, name='signup-done'),
	url(r'^signup/', views.signup_view, name='signup'),

	url(r'^logout/', views.logout_view, name='logout'),

	#url(r'^', include('django.contrib.auth.urls')),

	# TODO: Create our own views/forms for these.
	url(r'^change-password/$',
		auth_views.PasswordChangeView.as_view(),
		name='password_change'),

	url(r'^change-password/done/$',
		auth_views.PasswordChangeDoneView.as_view(),
		name='password_change_done'),

	url(r'^reset-password/$',
		auth_views.PasswordResetView.as_view(),
		name='password_reset'),

	url(r'^reset-password/done/$',
		auth_views.PasswordResetDoneView.as_view(),
		name='password_reset_done'),

	# I *think* this is how we'd capture base64?
	# and the site doesn't specify what format the "token" is
	url(r'^reset-password/(?P<uidb64>[0-9A-Za-z=]+)/(?P<token>[^/]+)/$',
		auth_views.PasswordResetConfirmView.as_view(),
		name='password_reset_confirm'),
]
