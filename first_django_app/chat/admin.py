from .models import Chat, Message, UserProfile
from django.contrib import admin

class MessageAdmin(admin.ModelAdmin):
    fields = ('chat', 'text', 'created_at', 'author', 'reciever')
    list_display = ('chat', 'text', 'created_at', 'author', 'reciever')
    
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)
admin.site.register(UserProfile)