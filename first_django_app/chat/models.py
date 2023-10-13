from datetime import date
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):   
    chat_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    users = models.ManyToManyField(User) 
    
   
class Message(models.Model):
    text=models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reciever_message_set')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
   
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)