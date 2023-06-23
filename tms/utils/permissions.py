from rest_framework import permissions


class IsRequestedUser(permissions.BasePermission):
    """
    Object-level permission
    """

    def has_object_permission(self, request, view, obj):
        # Instance must be of the User model.
        return obj.id == request.user.id
