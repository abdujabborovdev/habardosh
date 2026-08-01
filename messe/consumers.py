import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):

  async def connect(self):
    self.room_name = 'global_chat'
    self.room_group_name = 'chat_%s' % self.room_name

    # Foydalanuvchining IP manzilini olish
    headers = dict(self.scope['headers'])
    if b'x-forwarded-for' in headers:
      self.client_ip = headers[b'x-forwarded-for'].decode('utf-8').split(',')[0]
    else:
      self.client_ip = self.scope['client'][0]

    await self.channel_layer.group_add(
        self.room_group_name, self.channel_name
    )
    await self.accept()

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
        self.room_group_name, self.channel_name
    )

  async def receive(self, text_data):
    data = json.loads(text_data)
    message = data['message']
    username = data['username']

    # Xabarni IP manzili bilan birga bazaga saqlash
    await self.save_message(username, message, self.client_ip)

    await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',
            'message': message,
            'username': username,
            'ip_address': self.client_ip,  # IP ni ham hammaga yuborish mumkin (yoki faqat o'zingiz ko'rishingiz uchun qoldirish mumkin)
        },
    )

  async def chat_message(self, event):
    message = event['message']
    username = event['username']

    await self.send(
        text_data=json.dumps({'message': message, 'username': username})
    )

  @database_sync_to_async
  def save_message(self, username, message, ip_address):
    Message.objects.create(
        username=username, body=message, ip_address=ip_address
    )