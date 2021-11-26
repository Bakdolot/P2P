from rest_framework import permissions


class IsOwnerOrRecipient(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            login = request.user.login
            if login == obj.recipient:
                return request.method in permissions.SAFE_METHODS
            return obj.owner == login
        except AttributeError:
            return False


class IsRecipient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        login = request.user.login
        return login == obj.recipient