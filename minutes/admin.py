# Register your models here.
from django.contrib import admin

from .models import Folder, Meeting

admin.site.register(Folder)
admin.site.register(Meeting)
