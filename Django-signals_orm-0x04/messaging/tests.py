from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingSignalTest(TestCase):
    def test_notification_created_on_message(self):
        sender = User.objects.create_user(username='sender')
        receiver = User.objects.create_user(username='receiver')
        Message.objects.create(sender=sender, receiver=receiver, content="Hello")
        self.assertEqual(Notification.objects.filter(user=receiver).count(), 1)
