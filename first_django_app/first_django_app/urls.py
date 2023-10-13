"""
URL configuration for first_django_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from chat.views import chat_view, index, logIn,register, contacts


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('login/', logIn),
    path('register/', register),
    path('users/', contacts, name='user_list'),
    path('', RedirectView.as_view(url='/login/')),
    path('chat_view/', chat_view, name='chat_view'),
]
