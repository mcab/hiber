from rest_framework import permissions


class IsOwnerAndAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        return bool(request.user and request.user.is_authenticated) and (
            obj.watcher == request.user)
