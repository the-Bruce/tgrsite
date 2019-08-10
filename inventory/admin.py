from django.contrib import admin

from .models import Inventory, Loan, Record, Suggestion


class LoanAdmin(admin.ModelAdmin):
    model = Loan
    fields = ("requester", "inventory", "items", "start_date", "end_date", "authorised", "rejected", "taken_when",
              "taken_who", "returned_when", "returned_who", "notes", "state_text")
    readonly_fields = ('state_text',)


# Register your models here.
admin.site.register(Inventory)
admin.site.register(Record)
admin.site.register(Suggestion)
admin.site.register(Loan, LoanAdmin)
