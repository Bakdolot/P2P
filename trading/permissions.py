from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            login = request.user.login
            return obj.owner == login or obj.participant == login
        except AttributeError:
            return False


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            login = request.user.login
            return obj.owner == login
        except AttributeError:
            return False


class CustomIsAuthOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return bool(request.user.login)
        except AttributeError:
            return False


class IsParticipant(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            login = request.user.login
            return obj.participant == login
        except AttributeError:
            return False


class IsNotOwner(IsOwner):

    def has_object_permission(self, request, view, obj):
        return not super().has_object_permission(request, view, obj)
