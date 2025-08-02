from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(post_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id is None:
        # New message, not an edit
        return

    try:
        original = Message.objects.get(id=instance.id)
    except Message.DoesNotExist:
        return

    if original.content != instance.content:
        # Log the old content before saving new one
        MessageHistory.objects.create(
            message=instance,
            old_content=original.content
        )
        instance.edited = True  # Mark message as edited

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()


def notify_receiver(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
