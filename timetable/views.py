from django.views.generic import ListView, DetailView

from .models import Timetable


# Create your views here.
class TimetableView(ListView):
    template_name = "timetable/timetable.html"
    model = Timetable
    context_object_name = "timetables"

    def get_queryset(self):
        return Timetable.objects.filter(active=True)


class SingleTimetableView(DetailView):
    template_name = "timetable/single_timetable.html"
    model = Timetable
    context_object_name = "timetable"
