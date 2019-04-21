from django.contrib import admin

from .models import Inventory, Loan, Record, Suggestion

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Record)
admin.site.register(Suggestion)
admin.site.register(Loan)
