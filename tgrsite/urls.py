"""tgrsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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
	url(r'^notifications/', include('notify.urls')),

	# these are part of the users app
	# but I wanted the URLs to be eg /login rather than /user/login
	url(r'^login/', usersviews.login_view, name='login'),
	url(r'^login/done/', usersviews.login_process, name='login-done'),
	url(r'^logout/', usersviews.logout_view, name='logout'),

	# static pages ish
	# these will be located on the root path
	url(r'^', include('statics.urls')),
]
