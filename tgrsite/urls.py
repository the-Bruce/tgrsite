from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # the homepage is now a model and is located in pages.urls
    # to use it, create a Page model with the name "index"
    # url(r'^$', TemplateView.as_view(template_name='tgrsite/index.html'), name='homepage'),

    path('timetable/', include('timetable.urls')),
    path('admin/', admin.site.urls),
    path('forum/', include('forum.urls')),

    # hard redirect
    # url(r'^signups/(.*)', RedirectView.as_view(url='/events/', permanent=True)),

    # soft direct (/signups links still work but site universally links to /events)
    # url(r'^signups/', include('rpgs.urls')),

    path('events/', include('rpgs.urls'), name='rpgs_root'),
    path('exec/', include('exec.urls')),
    path('', include('users.urls')),
    path('messages/', include('messaging.urls')),
    path('bugs/', include('bugreports.urls')),
    path('newsletters/', include('newsletters.urls')),
    path('notifications/', include('notifications.urls')),

    # Pseudo "Static" pages - those with no models or fancy behaviour.
    # e.g. the larp intro page
    path('', include('statics.urls')),

    path('gallery/', include('gallery.urls')),

    # model-based pages, to supersede the statics module
    path('', include('pages.urls')),
]
