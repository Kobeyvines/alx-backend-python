from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own data.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthenticatedAndParticipant(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only participants can view, update, or delete
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE', 'POST']:
            return request.user in obj.participants.all()
        # For other methods, fallback to default
        return False