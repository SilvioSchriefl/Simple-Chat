
import uuid
from django.http import JsonResponse
from django.shortcuts import  get_object_or_404, render, redirect
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout





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
        existing_user = User.objects.filter(username=username).first()
        
        if existing_user:
            return render(request, 'chat/register.html', {'user_already_exist': True}) 
        
        elif password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect('/login/')  # Navigiere zur Startseite nach der Registrierung
        
        else:
            return render(request, 'chat/register.html', {'pw_not_match': True})
    return render(request, 'chat/register.html')

def contacts(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/users.html', {'users': users})



def chat_view(request):
    user_id = request.GET.get('user_id', None)
    current_user = request.user
    user = get_object_or_404(User, id=user_id)
    chat_exists = Chat.objects.filter(users=current_user).filter(users=user).exists()
    
    if request.method == 'POST':
        text_message = request.POST.get('text_message')
        if text_message.strip():
            chat_id = request.POST.get('chat_id', None)
            chat = get_object_or_404(Chat, chat_id=chat_id)
            new_message = Message.objects.create(author=request.user, reciever=user, text=text_message, chat=chat)
            new_message.save()
            serialized_message = {
                "author": current_user.username,
                "receiver": user.username,
                "text": new_message.text,
                "created_at": new_message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            return JsonResponse(serialized_message)
    
    
    if not chat_exists:
        chat = Chat.objects.create(chat_id=uuid.uuid4())
        chat.users.add(request.user, user)
        initial_message = "Hallo, dies ist der Start des Chats."
        new_message = Message.objects.create(author=request.user, reciever=user, text=initial_message, chat=chat)
        new_message.save()
        messages = chat.messages.all().order_by('created_at')
        return render(request, 'chat/chat_view.html', { 'messages': messages, 'chat': chat })
    else:
        chat = Chat.objects.filter(users=current_user).filter(users=user).first()
        chat_users = chat.users.all()
        messages = chat.messages.all().order_by('created_at')
        return render(request, 'chat/chat_view.html', { 'messages': messages, 'chat': chat, 'chat_users': chat_users, 'user_id': user_id})
    
def logout_view(request):
    logout(request)
    return render(request, 'chat/logout.html')  
   
        
    
        

        
    
    
    
