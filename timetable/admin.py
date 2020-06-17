from django.contrib import admin

from .models import Timetable, Booking, Event, Week, ColourScheme, GoogleCalender, RoomLink, SpecialEvent


# Register your models here.

class NewBookingInline(admin.StackedInline):
    model = Booking
    fields = ['room', 'event']
    extra = 6


class ChangeBookingInline(admin.StackedInline):
    model = Booking
    fields = ['room', 'event']
    extra = 1


class WeekAdmin(admin.ModelAdmin):
    model = Week
    inlines = []
    save_as = True
    save_on_top = True

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [ChangeBookingInline]
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = [NewBookingInline]
        return super().add_view(request, form_url, extra_context)


class TimetableAdmin(admin.ModelAdmin):
    model = Timetable


admin.site.register(SpecialEvent)
admin.site.register(Event)
admin.site.register(Week, WeekAdmin)
admin.site.register(ColourScheme)
admin.site.register(Timetable)
admin.site.register(GoogleCalender)
admin.site.register(RoomLink)
