from rest_framework.permissions import BasePermission


class ManagerPermission(BasePermission):

    def has_permission(self, request, view):
        is_manager = request.user.groups.filter(name='Managers').exists()
        if view.action in ('create', 'delete') and is_manager:
            return False
        return True


class OnlyManagerOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Managers').exists() or request.user == obj.user
