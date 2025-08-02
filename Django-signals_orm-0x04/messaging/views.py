# messaging/views.py
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Message
from django.shortcuts import render

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return JsonResponse({'message': 'User and related data deleted.'})


def threaded_messages(request):
    root_messages = Message.objects.filter(
        sender=request.user,
        parent_message__isnull=True
    ).select_related('receiver').prefetch_related('replies')

    threads = [get_thread(msg) for msg in root_messages]

    return render(request, 'messaging/threaded_messages.html', {'threads': threads})

def get_thread(message):
    thread = [message]
    for reply in message.replies.all():
        thread += get_thread(reply)
    return thread
