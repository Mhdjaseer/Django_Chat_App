import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room, Message
from django.contrib.auth import get_user_model


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

         # Get the room object
        room = Room.objects.get(name=self.room_name)

        # Get the sender information from the scope (assuming authentication is implemented)
        User = get_user_model()
        sender_id = self.scope['user'].id
        sender = User.objects.get(id=sender_id)
        sender_name = sender.username

        # Create and save the message to the database
        message_obj = Message(room=room, sender=sender, content=message)
        message_obj.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "username": sender_name
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "username": username}))