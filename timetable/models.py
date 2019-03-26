from datetime import date

from django.core import validators
from django.db import models


# Create your models here.
class Week(models.Model):
    startDate = models.CharField(max_length=10)
    number = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField(default=date.today().year,
                                            validators=[validators.MinValueValidator(2000, message="Invalid year")],
                                            help_text="Academic year (use greater year, i.e. 18/19 is 2019)")

    def __str__(self):
        return str(self.year) + " week " + str(self.number)

    class Meta:
        ordering = ['year', 'number']


class Event(models.Model):
    description = models.CharField(max_length=20)
    date_time_line = models.CharField(max_length=20)
    sort_key = models.SmallIntegerField()

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['sort_key']


class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    room = models.CharField(max_length=100)

    def __str__(self):
        return str(self.week) + ": " + str(self.event)


class Timetable(models.Model):
    title = models.CharField(max_length=30)
    events = models.ManyToManyField(Event)
    weeks = models.ManyToManyField(Week)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)
