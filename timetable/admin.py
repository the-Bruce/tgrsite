from django.contrib import admin

from .models import Timetable, Booking, Event, Week, ColourScheme


# Register your models here.

class BookingInline(admin.StackedInline):
    model = Booking
    fields = ['room', 'event']
    extra = 6

class WeekAdmin(admin.ModelAdmin):
    model = Week
    inlines = [BookingInline]

class TimetableAdmin(admin.ModelAdmin):
    model = Timetable

admin.site.register(Event)
admin.site.register(Week, WeekAdmin)
admin.site.register(ColourScheme)
admin.site.register(Timetable)
