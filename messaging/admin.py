from django.contrib import admin

from .models import MessageThread, Message

class MessageInline(admin.StackedInline):
	model = Message
	extra = 0
class MessageThreadAdmin(admin.ModelAdmin):
	inlines = [MessageInline]

admin.site.register(MessageThread, MessageThreadAdmin)
admin.site.register(Message)