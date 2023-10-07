from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import OnlyOwner
from users.serializers import UserSerializer, UserProfileSerializer


# class UserListAPIView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserRetrieveAPIView(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserCreateAPIView(CreateAPIView):
#     serializer_class = UserSerializer
#
#
# class UserUpdateAPIView(UpdateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDestroyAPIView(DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserViewSet(ModelViewSet):
    """
    Набор представлений действий с объектами модели юзера.

    Обновление и удаление разрешены только владельцам,
    создание разрешено любому пользователю,
    остальное доступно авторизованным пользователям
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsAuthenticated & OnlyOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = UserProfileSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = UserProfileSerializer
        return super().list(request, *args, **kwargs)

