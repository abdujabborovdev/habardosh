from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Message


def index(request):
  if request.method == 'POST':
    username = request.POST.get('username', '').strip()
    if username:
      request.session['username'] = username
      return redirect('chat')
  return render(request, 'index.html')


def chat_view(request):
  username = request.session.get('username')
  if not username:
    return redirect('index')

  # Bazadagi barcha eski xabarlarni chiqarish uchun
  messages = Message.objects.all().order_by('created')
  return render(
      request, 'chat.html', {'username': username, 'messages': messages}
  )


def send_message_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    body = request.POST.get('body', '')
    images = request.FILES.getlist('images')  # Bir nechta rasm uchun

    # Har bir rasm uchun alohida xabar yoki bitta xabarga biriktirib saqlash
    # Bu yerda oddiy qilib har bir rasm yoki matn saqlanadi
    message_objs = []

    if images:
      for img in images:
        msg = Message.objects.create(
            username=username, body=body if images.index(img) == 0 else '', image=img
        )
        message_objs.append(msg)
    else:
      msg = Message.objects.create(username=username, body=body)
      message_objs.append(msg)

    channel_layer = get_channel_layer()
    for msg in message_objs:
      image_url = msg.image.url if msg.image else None
      async_to_sync(channel_layer.group_send)(
          'chat_room_group', {
              'type': 'chat_message',
              'message': msg.body,
              'username': username,
              'image_url': image_url,
          }
      )

    return JsonResponse({'status': 'success'})

  return JsonResponse({'status': 'failed'}, status=400)