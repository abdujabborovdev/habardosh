from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message


def send_message_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    body = request.POST.get('body', '')
    image = request.FILES.get('image')

    # Bazaga saqlash
    message_obj = Message.objects.create(
        username=username, body=body, image=image
    )

    image_url = message_obj.image.url if message_obj.image else None

    # WebSocket orqali guruhdagi barchaga yuborish
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_room_group', {
            'type': 'chat_message',
            'message': body,
            'username': username,
            'image_url': image_url,
        }
    )

    return JsonResponse({'status': 'success', 'image_url': image_url})

  return JsonResponse({'status': 'failed'}, status=400)