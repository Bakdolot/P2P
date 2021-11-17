from rest_framework import permissions
from .trade_services import get_login


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            login = request.user.login
            return obj.owner == login
        except Exception as e:
            return False


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            login = request.user.login
            return obj.owner == login
        except Exception as e:
            return False


class CustomIsAuthOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return bool(request.user.login)
        except BaseException as e:
            return False


class IsParticipant(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            login = request.user.login
            return obj.participant == login
        except Exception as e:
            return False


class IsNotOwner(IsOwner):

    def has_object_permission(self, request, view, obj):
        return not super().has_object_permission(request, view, obj)


class IsStarted(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            if request.method in permissions.SAFE_METHODS:
                return True
            if obj.status == 'expectation':
                return True
            return False
        except Exception as e:
            return False
