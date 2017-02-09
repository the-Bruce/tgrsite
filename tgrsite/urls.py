from django.conf.urls import url, include
from django.contrib import admin
from . import views
from users import views as usersviews

urlpatterns = [
	url(r'^$', views.index, name='homepage'),
	url(r'^admin/', admin.site.urls),
	url(r'^forum/', include('forum.urls')),
	url(r'^rpg/', include('rpgs.urls')),
	url(r'^exec/', include('exec.urls')),
	url(r'^user/', include('users.urls')),
	url(r'^messages/', include('messaging.urls')),

	# these are part of the users app
	# but I wanted the URLs to be eg /login rather than /user/login
	url(r'^login/done/', usersviews.login_process, name='login-done'),
	url(r'^login/', usersviews.login_view, name='login'),

	url(r'^signup/done', usersviews.signup_process, name='signup-done'),
	url(r'^signup/', usersviews.signup_view, name='signup'),

	url(r'^logout/', usersviews.logout_view, name='logout'),

	# static pages ish
	# these will be located on the root path
	url(r'^', include('statics.urls')),

]
