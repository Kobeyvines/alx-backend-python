from rest_framework import viewsets, status, filters, generics  # <-- add filters here
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner, IsAuthenticatedAndParticipant

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticatedAndParticipant]
    filter_backends = [filters.OrderingFilter]  # <-- example use of filters
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedAndParticipant]
    filter_backends = [filters.OrderingFilter]  # <-- example use of filters
    ordering_fields = ['sent_at']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)
