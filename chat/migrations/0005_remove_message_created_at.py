# Generated by Django 4.2.2 on 2023-06-11 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_message_created_at_message_liked_by_message_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='created_at',
        ),
    ]
