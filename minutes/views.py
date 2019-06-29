from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, CreateView

from .models import Folder, Meeting
from .forms import MeetingForm


# Create your views here.
class MeetingDetail(DetailView):
    model = Meeting
    template_name = "minutes/detail.html"

    def get_queryset(self):
        super().get_queryset()
        folders = Folder.roots()
        folder = None
        for i in self.kwargs['folder'].split("/"):
            try:
                folder = folders.get(name__iexact=i)
                folders = folder.children.all()
            except (Folder.MultipleObjectsReturned, Folder.DoesNotExist):
                Http404("Unknown folder")
        if folder is None:
            Http404("Unknown folder")
        return folder.meetings.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            item = queryset.get(name__iexact=self.kwargs['name'])
        except ObjectDoesNotExist:
            raise Http404("No meeting found with that address")
        except MultipleObjectsReturned:
            raise Http404("Ambiguous record: please refine")

        return item

    def get(self, request, *args, **kwargs):
        print(self.kwargs['folder'])
        return super().get(request, *args, **kwargs)


class CreateMeeting(PermissionRequiredMixin, CreateView):
    permission_required = "minutes:add_meeting"
    model = Meeting
    form_class = MeetingForm
    template_name = "minutes/edit.html"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user.member
        return super().form_valid(form)


def meetingBounce(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    return HttpResponseRedirect(meeting.get_absolute_url())


def index(request):
    meeting = Meeting.objects.latest(field_name="date")
    return HttpResponseRedirect(meeting.get_absolute_url())
