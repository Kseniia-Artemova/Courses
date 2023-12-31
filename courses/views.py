import requests
from django.http import HttpRequest
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from courses.services import payments
from courses.models import Course, Lesson, Payment, Subscription
from courses.pagination import SimplePageNumberPagination
from courses.permissions import IsManager, OnlyManagerOrOwner, OnlyOwner
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from courses.tasks import task_send_updates


class CourseListAPIView(ListAPIView):
    """
    Представление для просмотра списка курсов.
    Юзеры могут видеть только свои курсы, менеджеры могут видеть весь список.
    Запрещено для неавторизованных пользователей
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SimplePageNumberPagination

    # def get_queryset(self):
    #     if not self.request.user.groups.filter(name='Managers').exists():
    #         self.queryset = Course.objects.filter(user=self.request.user)
    #     else:
    #         self.queryset = Course.objects.all()
    #     queryset = super().get_queryset()
    #
    #     return queryset


class CourseRetrieveAPIView(RetrieveAPIView):
    """
    Представление для просмотра конкретного объекта курса.
    Юзеры могут видеть только свои курсы, менеджеры могут видеть любые.
    Запрещено для неавторизованных пользователей
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & OnlyManagerOrOwner]


class CourseCreateAPIView(CreateAPIView):
    """
    Представление для создания объекта курса.
    Запрещено для менеджеров и неавторизованных пользователей
    """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & ~IsManager]

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

    def perform_update(self, serializer):
        course = self.get_object()
        time_between_updates = (timezone.now() - course.last_update).seconds
        time_in_hours = time_between_updates // 3600
        serializer.save()

        if time_in_hours >= 4:
            total_url = self.request.build_absolute_uri(reverse('courses:course_detail', kwargs={'pk': course.pk}))
            task_send_updates.delay(course.pk, total_url)


class CourseDestroyAPIView(DestroyAPIView):
    """
    Представление для удаления объекта курса.
    Запрещено для менеджеров и неавторизованных пользователей
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & OnlyOwner]


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
    pagination_class = SimplePageNumberPagination
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated & ~IsManager]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated & OnlyOwner]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & OnlyManagerOrOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     if not self.request.user.groups.filter(name='Managers').exists():
    #         self.queryset = Lesson.objects.filter(user=self.request.user)
    #     else:
    #         self.queryset = Lesson.objects.all()
    #     queryset = super().get_queryset()
    #
    #     return queryset


class PaymentListAPIView(ListAPIView):
    """
    Представление для отображения списка платежей.

    Менеджеры могут видеть весь список, обычные юзеры - только свои платежи
    """

    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('course', 'way_pay')
    ordering_fields = ('date',)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.groups.filter(name='Managers').exists():
            self.queryset = Payment.objects.filter(user=self.request.user)
        else:
            self.queryset = Payment.objects.all()
        queryset = super().get_queryset()

        return queryset


class PaymentRetrieveAPIView(RetrieveAPIView):
    """
    Представление для отображения конкретного платежа.

    Менеджеры могут видеть любой платёж, обычные юзеры - только свои платежи
    """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated & OnlyManagerOrOwner]
    queryset = Payment.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_to_updates(request: HttpRequest, pk: int) -> Response:
    """
    Представление для осуществления подписки на обновления курса или отмены подписки.
    Запрещено неавторизованным пользователям
    """

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Такой курс не существует."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if Subscription.objects.filter(course=course, user=request.user).exists():
            Subscription.objects.filter(course=course, user=request.user).delete()
            return Response({'message': f'Подписка на обновления курса {course.name} отменена!'},
                            status=status.HTTP_200_OK)

        data = {'course': pk, 'user': request.user.id}
        serializer = SubscriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Подписан на обновления курса {course.name}!'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pay_course(request: HttpRequest, course_pk: int) -> Response:
    """
    Представление для получения ссылки оплаты за курс, сразу перенаправляет на создание платежа.
    Создаёт неактивный платёж.
    Права доступа по умолчанию - только для авторизованных пользователей
    """

    try:
        course = Course.objects.get(pk=course_pk)
        if course:
            session_id, payment_url = payments.get_payment_link(request, course)
            data = {
                'amount': course.price,
                'user': request.user.pk,
                'course': course.pk,
                'id_stripe_session': session_id
            }
            print(session_id, payment_url)
            serializer = PaymentSerializer(data=data)
            if serializer.is_valid():
                print(serializer)
                serializer.save()
                return Response({"payment_url": payment_url}, status=status.HTTP_200_OK)

    except requests.RequestException as error:
        return Response({"error": "Ошибка доступа к сайту оплаты"}, status=status.HTTP_400_BAD_REQUEST)

    except Course.DoesNotExist:
        return Response({"error": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)
