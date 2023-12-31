from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Права менеджеров
    Имеют доступ ко всему, кроме создания и удаления объектов
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Managers').exists()


class OnlyManagerOrOwner(BasePermission):
    """
    Права, дающие доступ для менеджеров или создателей объекта
    """

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Managers').exists() or request.user == obj.user


class OnlyOwner(BasePermission):
    """
    Права, дающие доступ только для создателей объекта
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
