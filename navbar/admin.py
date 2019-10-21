from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin
from .models import BarItem, DropDownItem, BarDropdown


class DropdownList(StackedInline):
    model = DropDownItem
    extra = 1

class BarItemAdmin(ModelAdmin):
    list_display = ("text", "sort_index", "target")

class BarDropdownAdmin(ModelAdmin):
    model = BarDropdown
    inlines = [DropdownList]
    list_display = ("text", "sort_index")


# Register your models here.
admin.site.register(BarItem, BarItemAdmin)
admin.site.register(BarDropdown, BarDropdownAdmin)
