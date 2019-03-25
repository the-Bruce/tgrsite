from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(template_name='bugreports/index.html'), name='bug_index'),
    url(r'^(?P<pk>[0-9]+)', views.Detail.as_view(), name='bug_detail'),
    url(r'^create$', views.Create.as_view(), name='bug_create'),
]
