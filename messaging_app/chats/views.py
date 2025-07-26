from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsAuthenticatedAndParticipant
from django.shortcuts import get_object_or_404

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticatedAndParticipant]

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedAndParticipant]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        if not conversation_id:
            return Response(
                {"error": "Conversation ID is required"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation = get_object_or_404(
            Conversation, 
            id=self.kwargs.get('conversation_pk')
        )
        if self.request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant of this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )