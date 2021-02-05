from django.contrib import admin

from .models import MessageThread, MessageReport


# these settings would give admins access to all DMs
# class MessageInline(admin.StackedInline):
#	model = Message
#	extra = 0
# class MessageThreadAdmin(admin.ModelAdmin):
#	inlines = [MessageInline]
# admin.site.register(MessageThread, MessageThreadAdmin)
# admin.site.register(Message)

class MessageReportAdmin(admin.ModelAdmin):
    readonly_fields = ['member', 'message', 'time', 'comment']
    list_display = ['member', 'time','message']


# more sensible, though might still need to be removed
admin.site.register(MessageThread)
admin.site.register(MessageReport, MessageReportAdmin)
