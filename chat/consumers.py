from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room, Message
from django.contrib.auth import get_user_model
import json
from datetime import datetime

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

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'like' in text_data_json:
            message_id = text_data_json['message_id']
            message = Message.objects.get(id=message_id)
            sender = self.scope['user']

            if sender in message.liked_by.all():
                message.liked_by.remove(sender)
                message.likes -= 1
            else:
                message.liked_by.add(sender)
                message.likes += 1

            message.save()

            # Send updated like count to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': 'chat_message',
                    'like': True,
                    'message_id': message_id,
                    'likes': message.likes
                }
            )
        else:
            message = text_data_json['message']

            # Get the room object
            room = Room.objects.get(name=self.room_name)

            # Get the sender information
            sender_id = self.scope['user'].id
            sender = get_user_model().objects.get(id=sender_id)
            sender_name = sender.username

            # Create and save the message to the database
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message_obj = Message(room=room, sender=sender, content=message, timestamp=timestamp)
            message_obj.save()

            # Update the UserMessage objects for the users in the room
           

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    'type': 'chat_message',
                    'message': message,
                    'username': sender_name,
                    'message_id': message_obj.id,
                    'timestamp': timestamp,
                    'notification': True  # Add a notification flag
                }
            )
    def chat_message(self, event):
        if 'like' in event:
            message_id = event['message_id']
            message = Message.objects.get(id=message_id)

            self.send(text_data=json.dumps({
                'like': True,
                'message_id': message.id,
                'likes': message.likes
            }))
        else:
            message = event['message']
            username = event['username']

            notification = False
            if 'notification' in event and event['notification']:
                notification = True
            

            self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'notification': notification  # Send the notification flag to the client
            }))
