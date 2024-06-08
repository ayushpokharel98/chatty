# main/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from main.models import Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['room_name']
        self.chat_group_name = f'chat_{self.chat_name}'

        # Join chat group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        try:
            message = data['message']
            username = data['username']
        except KeyError as e:
            print(f"KeyError: {e}")
            return

        # Save the message to the database
        await self.save_message(username, message)

        # Send message to WebSocket group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, username, message):
        user = User.objects.get(username=username)
        chats = Chat.objects.filter(chat_name=self.chat_name).first()
        Message.objects.create(chat=chats, sender=user, content=message)
