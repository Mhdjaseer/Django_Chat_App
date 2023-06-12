from datetime import timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from chat.models import Room, Message

User = get_user_model()

class RoomModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

    def test_room_creation(self):
        room = Room.objects.create(name='Test Room')
        room.users.set([self.user1, self.user2])  # Use set() instead of add() to set multiple users
        self.assertEqual(room.name, 'Test Room')
        self.assertEqual(room.users.count(), 2)

class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.room = Room.objects.create(name='Test Room')
    
    def test_message_creation(self):
        message = Message.objects.create(room=self.room, sender=self.user, content='Test message')
        self.assertEqual(message.room, self.room)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.content, 'Test message')

    def test_message_deletability(self):
        message = Message.objects.create(room=self.room, sender=self.user, content='Test message')
        self.assertTrue(message.is_deletable())

        # Change the created_at time to be older than 10 minutes
        message.created_at -= timedelta(minutes=11)
        message.save()
        self.assertFalse(message.is_deletable())
