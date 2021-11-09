from rest_framework import permissions
from .trade_services import get_login


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            login = get_login(request.META.get('HTTP_AUTHORIZATION').split(' ')[1])
            return obj.owner == login
        except Exception as e:
            return False