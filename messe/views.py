from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Message


def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip


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

  messages = Message.objects.all().order_by('created')
  return render(
      request, 'chat.html', {'username': username, 'messages': messages}
  )


def send_message_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    body = request.POST.get('body', '')
    images = request.FILES.getlist('images')
    client_ip = get_client_ip(request)

    message_objs = []
    if images:
      for img in images:
        msg = Message.objects.create(
            username=username,
            body=body if images.index(img) == 0 else '',
            image=img,
            ip_address=client_ip,
        )
        message_objs.append(msg)
    else:
      msg = Message.objects.create(
          username=username, body=body, ip_address=client_ip
      )
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


def online_users_view(request):
  users_data = (
      Message.objects.values('username', 'ip_address', 'created')
      .distinct()
      .order_by('-created')
  )
  return render(request, 'users_list.html', {'users_data': users_data})