from django.contrib import admin

from .models import Redirect

class RedirectAdmin(admin.ModelAdmin):
    list_display = ["source", "sink"]
    readonly_fields = ["usages", "url"]

# Register your models here.
admin.site.register(Redirect, RedirectAdmin)