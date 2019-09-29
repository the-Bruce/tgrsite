from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin
from .models import BarItem, DropDownItem, BarDropdown


class DropdownList(StackedInline):
    model = DropDownItem
    extra = 1


class BarDropdownAdmin(ModelAdmin):
    model = BarDropdown
    inlines = [DropdownList]


# Register your models here.
admin.site.register(BarItem)
admin.site.register(BarDropdown, BarDropdownAdmin)
#admin.site.register(DropDownItem)
