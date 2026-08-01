from django.shortcuts import redirect, render
from .models import Message


def index_view(request):
  if request.method == 'POST':
    username = request.POST.get('username').strip()
    if username:
      # Agar bu ism allaqachon sessionda yoki chatda band qilingan bo'lsa
      # (Oddiy mantiqda hozircha session orqali tekshiramiz)
      request.session['username'] = username
      return redirect('chat')
  return render(request, 'index.html')


def chat_view(request):
  username = request.session.get('username')
  if not username:
    return redirect('index')

  messages = Message.objects.all().order_by('created')
  return render(request, 'chat.html', {'username': username, 'messages': messages})