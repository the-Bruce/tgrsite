from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.index, name='homepage'),
	url(r'^admin/', admin.site.urls),
	url(r'^forum/', include('forum.urls')),
	url(r'^rpg/', include('rpgs.urls')),
	url(r'^exec/', include('exec.urls')),
	url(r'^', include('users.urls')),
	url(r'^messages/', include('messaging.urls')),
	url(r'^bugs/', include('bugreports.urls')),
	# static pages ish
	# these will be located on the root path
	url(r'^', include('statics.urls')),

]
