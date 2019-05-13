from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Folder, Meeting


# Create your views here.
class MeetingDetail(DetailView):
    model = Meeting
    template_name = "minutes/detail.html"

    def get_queryset(self):
        qs=super().get_queryset()
        folders=Folder.objects
        for i in self.kwargs['folder'].split("/"):
            pass



    def get_object(self, queryset=None):
        if queryset is None:
            queryset=self.get_queryset()

        try:
            item=queryset.get(name__iexact=self.kwargs['name'])
        except ObjectDoesNotExist:
            raise Http404("No meeting found with that address")
        except MultipleObjectsReturned:
            raise Http404("Ambigous record: please refine")

        return item


    def get(self, request, *args, **kwargs):
        print(self.kwargs['folder'])
        return super().get(request, *args, **kwargs)


def meetingBounce(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    return HttpResponseRedirect(meeting.get_absolute_url())
