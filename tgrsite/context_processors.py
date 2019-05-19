from django.conf import settings  # import the settings file

from forum.models import Thread, Response


def add_debug(request):
    return {'DEBUG': settings.DEBUG}


def latestposts(request):
    return {
        'latestthreads': Thread.objects.order_by('-pub_date')[:5],
        'latestresponses': Response.objects.order_by('-pub_date')[:5],
    }
