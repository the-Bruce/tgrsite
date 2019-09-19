from django.contrib import admin

from .models import Timetable, Booking, Event, Week, ColourScheme, GoogleCalender, RoomLink


# Register your models here.

class NewBookingInline(admin.StackedInline):
    model = Booking
    fields = ['room', 'event']
    extra = 6


class ChangeBookingInline(admin.StackedInline):
    model = Booking
    fields = ['room', 'event']
    extra = 0


class WeekAdmin(admin.ModelAdmin):
    model = Week
    inlines = []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [ChangeBookingInline]
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = [NewBookingInline]
        return super().add_view(request, form_url, extra_context)


class TimetableAdmin(admin.ModelAdmin):
    model = Timetable


admin.site.register(Event)
admin.site.register(Week, WeekAdmin)
admin.site.register(ColourScheme)
admin.site.register(Timetable)
admin.site.register(GoogleCalender)
admin.site.register(RoomLink)
