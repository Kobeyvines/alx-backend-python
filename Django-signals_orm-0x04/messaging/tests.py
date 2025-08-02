from django.test import TestCase
from django.contrib.auth.models import User
from messaging.models import Message, Notification

class UserDeletionSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

        # ✅ Create a real Message instance
        self.message = Message.objects.create(
            sender=self.user,
            receiver=self.receiver,
            content="Hello!"
        )

        # ✅ Pass the actual Message instance to Notification
        self.notification = Notification.objects.create(
            user=self.receiver,
            message=self.message
        )

    def test_user_deletion_cascades(self):
        self.user.delete()

        # Check if message and notification are also deleted
        self.assertFalse(Message.objects.filter(pk=self.message.pk).exists())
        self.assertFalse(Notification.objects.filter(pk=self.notification.pk).exists())
