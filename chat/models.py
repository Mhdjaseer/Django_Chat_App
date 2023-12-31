from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Room(models.Model):
    name = models.CharField(unique=True, max_length=255)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(get_user_model(), related_name='liked_messages')
    created_at = models.DateTimeField(default=timezone.now)
    reported = models.BooleanField(default=False)
    def __str__(self):
        return f'Message by {self.sender.username} in {self.room.name}'

    def is_deletable(self):
        time_difference = timezone.now() - self.created_at
        return time_difference.total_seconds() <= 600  # 10 minutes (10 minutes * 60 seconds)