from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


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
    queryset = User.objects.all()
    serializer_class = UserSerializer
