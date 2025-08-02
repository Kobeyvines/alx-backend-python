from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

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



def notify_receiver(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
