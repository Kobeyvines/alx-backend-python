from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsAuthenticatedAndParticipant
from .filters import MessageFilter
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND
)

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
        return Response(serializer.data, status=HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.participants.all():
            raise PermissionDenied("You are not a participant of this conversation")

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
            return Message.objects.none()
        
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(
                detail="You are not a participant of this conversation",
                code=HTTP_403_FORBIDDEN
            )
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation = get_object_or_404(
            Conversation, 
            id=self.kwargs.get('conversation_pk')
        )
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(
                detail="You are not a participant of this conversation",
                code=HTTP_403_FORBIDDEN
            )
        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )
        return Response(serializer.data, status=HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)