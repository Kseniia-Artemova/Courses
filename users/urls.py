from rest_framework.routers import DefaultRouter
from django.urls import path
from users.apps import UsersConfig
from users.views import UserViewSet
# from users.views import UserListAPIView, UserRetrieveAPIView, UserCreateAPIView, UserUpdateAPIView, UserDestroyAPIView

name_app = UsersConfig.name

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    # path('list/', UserListAPIView.as_view(), name='users_list'),
    # path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    # path('create/', UserCreateAPIView.as_view(), name='user_create'),
    # path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    # path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
] + router.urls