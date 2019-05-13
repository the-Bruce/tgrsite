from django.contrib import admin

# Register your models here.
from .models import StringProperty, TextProperty

admin.site.register(StringProperty)
admin.site.register(TextProperty)
