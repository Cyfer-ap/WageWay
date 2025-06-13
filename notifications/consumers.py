import json
from channels.generic.websocket import AsyncWebsocketConsumer
from users.utils import set_user_online
from notifications.models import Message  # <-- Import your Message model
from users.models import User
from asgiref.sync import sync_to_async
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_name = f"chat_{min(self.user.id, int(self.other_user_id))}_{max(self.user.id, int(self.other_user_id))}"
        self.room_group_name = self.room_name

        set_user_online(self.user)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get('typing'):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_notification',
                    'sender': data['sender']
                }
            )
        else:
            # Save message to DB
            await self.save_message(
                sender=self.scope['user'].id,
                receiver=int(self.other_user_id),
                content=data['message']
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data['message'],
                    'sender': data['sender'],
                    'timestamp': data['timestamp']
                }
            )

    @sync_to_async
    def save_message(self, sender, receiver, content):
        sender_user = User.objects.get(id=sender)
        receiver_user = User.objects.get(id=receiver)
        Message.objects.create(
            sender=sender_user,
            receiver=receiver_user,
            content=content,
            timestamp=timezone.now()
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))

    async def typing_notification(self, event):
        await self.send(text_data=json.dumps({
            'typing': True,
            'sender': event['sender']
        }))
