from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

class ChatroomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from django.contrib.auth.models import User
        from .models import ChatGroup, Message

        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.room_group_name = f'chat_{self.chatroom_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        from django.contrib.auth.models import User
        from .models import ChatGroup, Message

        data = json.loads(text_data)
        message = data['message']
        sender_username = data['sender']

        await self.save_message(sender_username, self.chatroom_name, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @database_sync_to_async
    def save_message(self, sender_username, chatroom_name, message):
        from django.contrib.auth.models import User
        from .models import ChatGroup, Message

        sender = User.objects.get(username=sender_username)
    
        user_id_1, user_id_2 = map(int, chatroom_name.split('_')[-2:])
    
        user1 = User.objects.get(id=user_id_1)
        user2 = User.objects.get(id=user_id_2)

        chat, _ = ChatGroup.objects.get_or_create(
            user1=min(user1, user2, key=lambda u: u.id),
            user2=max(user1, user2, key=lambda u: u.id)
        )

        Message.objects.create(chat=chat, sender=sender, content=message)
