from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson, Payment
from courses.permissions import ManagerPermission, OnlyManagerOrOwner, OnlyOwner
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseListAPIView(ListAPIView):
    """
    Представление для просмотра списка курсов.
    Юзеры могут видеть только свои курсы, менеджеры могут видеть весь список.
    Запрещено для неавторизованных пользователей
    """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    action = 'list'

    def get_queryset(self):
        if not self.request.user.groups.filter(name='Managers').exists():
            self.queryset = Course.objects.filter(user=self.request.user)
        else:
            self.queryset = Course.objects.all()
        queryset = super().get_queryset()

        return queryset


class CourseRetrieveAPIView(RetrieveAPIView):
    """
    Представление для просмотра конкретного объекта курса.
    Юзеры могут видеть только свои курсы, менеджеры могут видеть любые.
    Запрещено для неавторизованных пользователей
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & OnlyManagerOrOwner]
    action = 'retrieve'


class CourseCreateAPIView(CreateAPIView):
    """
    Представление для создания объекта курса.
    Запрещено для менеджеров и неавторизованных пользователей
    """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & ManagerPermission]
    action = 'create'

    def perform_create(self, serializer):
        new_object = serializer.save()
        new_object.user = self.request.user
        new_object.save()


class CourseUpdateAPIView(UpdateAPIView):
    """
    Представление для редактирования объекта курса.
    Юзеры могут редактировать только свои курсы, менеджеры могут редактировать любые.
    Запрещено для неавторизованных пользователей
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & OnlyManagerOrOwner]
    action = 'update'


class CourseDestroyAPIView(DestroyAPIView):
    """
    Представление для удаления объекта курса.
    Запрещено для менеджеров и неавторизованных пользователей
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & OnlyOwner]
    action = 'destroy'


class LessonViewSet(ModelViewSet):
    """
    Набор представлений для модели урока.

    Удаление и создание запрещено для менеджеров,
    изменение и детальный просмотр разрешены для менеджеров и владельцев,
    просмотр списка разрешен любым авторизованным пользователям.
    Список объектов ограничен для обычных юзеров собственными объектами,
    для менеджеров доступен весь список объектов
    """

    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ('list', 'create'):
            permission_classes = [IsAuthenticated & ManagerPermission]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated & OnlyOwner]
        else:
            permission_classes = [IsAuthenticated & OnlyManagerOrOwner]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        if not self.request.user.groups.filter(name='Managers').exists():
            self.queryset = Lesson.objects.filter(user=self.request.user)
        else:
            self.queryset = Lesson.objects.all()
        queryset = super().get_queryset()

        return queryset


class PaymentListAPIView(ListAPIView):
    """
    Представление для отображения списка объектов.

    Менеджеры могут видеть весь список, обычные юзеры - только свои платежи
    """

    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('course', 'lesson', 'way_pay')
    ordering_fields = ('date',)
    permission_classes = [IsAuthenticated]
    action = 'list'

    def get_queryset(self):
        if not self.request.user.groups.filter(name='Managers').exists():
            self.queryset = Payment.objects.filter(user=self.request.user)
        else:
            self.queryset = Payment.objects.all()
        queryset = super().get_queryset()

        return queryset
