from django.views.generic import ListView, DetailView

from .models import Timetable, GoogleCalender


# Create your views here.
class TimetableView(ListView):
    template_name = "timetable/timetable.html"
    model = Timetable
    context_object_name = "timetables"

    def get_queryset(self):
        return Timetable.objects.filter(active=True)

    def get_context_data(self, *args, **kwargs):
        ctxt = super().get_context_data(*args, **kwargs)
        ctxt['google_cals'] = GoogleCalender.objects.all().order_by('sort')
        return ctxt


class SingleTimetableView(DetailView):
    template_name = "timetable/single_timetable.html"
    model = Timetable
    context_object_name = "timetable"


# Create your views here.
class SubscribeView(ListView):
    template_name = "timetable/subscribe.html"
    model = GoogleCalender
    context_object_name = "google_cals"

    def get_queryset(self):
        return GoogleCalender.objects.all().order_by('sort')
