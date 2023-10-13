
import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import  get_object_or_404, render, redirect
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q



@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        chatID = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['text_message'], chat=chatID, author=request.user, reciever=request.user)
    chatMessages = Message.objects.filter(chat__id=1)    
    return render(request, 'chat/index.html', {'messages': chatMessages})

def logIn(request):
    if request.method == 'POST':
        user = authenticate(username = request.POST.get('user_name'), password = request.POST.get('password'))
        if user :
            login (request, user)
            return redirect('/users/') 
        else : 
            return render(request, 'chat/login.html', {'wrongPassword': True})
    return render(request, 'chat/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect('/login/')  # Navigiere zur Startseite nach der Registrierung
        else:
            return render(request, 'chat/register.html', {'error': True})
    return render(request, 'chat/register.html')

def contacts(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/users.html', {'users': users})



def chat_view(request):
    user_id = request.GET.get('user_id', None)
    current_user = request.user
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id', None)
        chat = get_object_or_404(Chat, chat_id=chat_id)
        new_message = Message.objects.create(author=current_user, reciever=user, text=request.POST['text_message'], chat=chat)
        new_message.save()
        messages = chat.messages.all().order_by('created_at')
        
    chat_exists = Chat.objects.filter(users=current_user).filter(users=user).exists()
    if not chat_exists:
        # Wenn kein Chat existiert, erstellen Sie einen neuen Chat
        chat = Chat.objects.create(chat_id=uuid.uuid4())
        chat.users.add(request.user, user)
        initial_message = "Hallo, dies ist der Start des Chats."
        new_message = Message.objects.create(author=request.user, receiver=user, text=initial_message, chat=chat)
        new_message.save()
        messages = chat.messages.all().order_by('created_at')
        return render(request, 'chat/chat_view.html', { 'messages': messages, 'chat': chat })
    else:
        chat = Chat.objects.filter(users=current_user).filter(users=user).first()
        chat_users = chat.users.all()
        messages = chat.messages.all().order_by('created_at')
        return render(request, 'chat/chat_view.html', { 'messages': messages, 'chat': chat, 'chat_users': chat_users, 'user_id': user_id})

        
    
    
    
