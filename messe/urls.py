from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chat'),
    path('send-message/', views.send_message_view, name='send_message'),
    path('users/', views.online_users_view, name='users_list'),
]