from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsAuthenticatedAndParticipant
from .filters import MessageFilter
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling conversation operations
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticatedAndParticipant]

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling message operations within conversations
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedAndParticipant]
    filterset_class = MessageFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        if not conversation_id:
            return Message.objects.none()  # Return empty queryset instead of Response
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation = get_object_or_404(
            Conversation, 
            id=self.kwargs.get('conversation_pk')
        )
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation")
        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )