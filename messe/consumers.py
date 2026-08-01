import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = 'global_chat'
        self.room_group_name = 'chat_%s' % self.room_name

        # Guruhga qo'shilish
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Guruhdan chiqish
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Xabarni bazaga saqlash
        await self.save_message(username, message)

        # Xabarni guruhdagi barchaga yuborish
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Brauzerga ma'lumotni yuborish
        await self.send(
            text_data=json.dumps({
                'message': message,
                'username': username
            })
        )

    @database_sync_to_async
    def save_message(self, username, message):
        Message.objects.create(username=username, body=message)