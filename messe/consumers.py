import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

  async def connect(self):
    self.room_name = 'chat_room'
    self.room_group_name = 'chat_room_group'

    # Chat guruhiga qo'shilish
    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
    await self.accept()

  async def disconnect(self, close_code):
    # Guruhdan chiqish
    await self.channel_layer.group_discard(
        self.room_group_name, self.channel_name
    )

  # Brauzerdan xabar kelganda ishlaydi (faqat matn uchun)
  async def receive(self, text_data):
    data = json.loads(text_data)
    message = data.get('message', '')
    username = data.get('username', '')

    # Guruhdagi barcha foydalanuvchilarga xabarni tarqatish
    await self.channel_layer.group_send(
        self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'username': username,
            'image_url': None,
        }
    )

  # Guruhdan xabar kelganda uni brauzerga chiqarish
  async def chat_message(self, event):
    await self.send(
        text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'image_url': event.get('image_url'),
        })
    )