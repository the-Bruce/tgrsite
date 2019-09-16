from django.shortcuts import HttpResponseRedirect, HttpResponsePermanentRedirect, get_object_or_404

from .models import Redirect


# Create your views here.
def redirect(request, source):
    sink = get_object_or_404(Redirect, source__iexact=source)
    if sink.permanent:
        return HttpResponsePermanentRedirect(sink.sink)
    else:
        return HttpResponseRedirect(sink.sink)
