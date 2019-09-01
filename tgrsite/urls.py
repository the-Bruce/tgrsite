from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from redirect.views import redirect


# the homepage is now a model and is located in pages.urls
# to use it, create a Page model with the name "index"
# url(r'^$', TemplateView.as_view(template_name='tgrsite/index.html'), name='homepage'),
urlpatterns = [
    path('timetable/', include('timetable.urls')),
    path('admin/', admin.site.urls),
    path('forum/', include('forum.urls')),
    path('events/', include('rpgs.urls'), name='rpgs_root'),
    path('exec/', include('exec.urls')),
    path('', include('users.urls')),
    path('messages/', include('messaging.urls')),
    path('newsletters/', include('newsletters.urls')),
    path('notifications/', include('notifications.urls')),
    path('inventory/', include('inventory.urls')),
    path('minutes/', include('minutes.urls')),
    path('gallery/', include('gallery.urls')),
    path('', include('pages.urls')),
    path('<slug:source>/', redirect)
] + static(settings.MEDIA_URL,
     document_root=settings.MEDIA_ROOT)  # This only runs if DEBUG=True. Its a bad idea on prod
