from django.urls import path, include
from rest_framework import routers  # <-- ensure this import is here
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()  # <-- match the required string

router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
