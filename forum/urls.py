from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='forum'),
    url(r'^(?P<pk>[0-9]+)/$', views.forum, name='subforum'),
    # url(
    #	r'^thread/(?P<pk>[0-9]+)/#response-(?P<response_id>[0-9]+)/$',
    #	views.thread,
    #	name='viewresponse'
    # ),
    url(
        r'^thread/(?P<pk>[0-9]+)/$',
        views.thread,
        name='viewthread'
    ),

    url(
        r'^thread/respond/$',
        views.create_response,
        name='createresponse'
    ),

    url(r'^thread/create', views.create_thread, name='createthread'),

    url(
        r'^thread/(?P<pk>[0-9]+)/delete$',
        views.delete_thread,
        name='thread_delete'
    ),

    url(
        r'^thread/(?P<pk>[0-9]+)/edit$',
        views.edit_thread_view,
        name='thread_edit'
    ),

    url(
        r'^thread/edit/done$',
        views.edit_thread_process,
        name='thread_edit_done'
    ),

    url(
        r'^response/(?P<pk>[0-9]+)/delete$',
        views.delete_response,
        name='response_delete'
    ),

    url(
        r'^response/(?P<pk>[0-9]+)/edit$',
        views.edit_response_view,
        name='response_edit'
    ),

    url(
        r'^response/edit/done$',
        views.edit_response_process,
        name='response_edit_done'
    ),

]
