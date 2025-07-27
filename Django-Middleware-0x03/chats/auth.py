from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes obj has a 'participants' attribute (e.g., a ManyToMany to User)
        return request.user in obj.participants.all()