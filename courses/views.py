from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson, Payment
from courses.permissions import ManagerPermission, OnlyManagerOrOwner
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseListAPIView(ListAPIView):
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
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & OnlyManagerOrOwner]
    action = 'retrieve'


class CourseCreateAPIView(CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & ManagerPermission]
    action = 'create'

    def perform_create(self, serializer):
        new_object = serializer.save()
        new_object.user = self.request.user
        new_object.save()


class CourseUpdateAPIView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & OnlyManagerOrOwner]
    action = 'update'


class CourseDestroyAPIView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated & OnlyManagerOrOwner]
    action = 'destroy'


class LessonViewSet(ModelViewSet):
    # queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & OnlyManagerOrOwner]

    def get_permissions(self):
        if self.action in ('list', 'create', 'destroy'):
            permission_classes = [IsAuthenticated & ManagerPermission]
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
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('course', 'lesson', 'way_pay')
    ordering_fields = ('date',)
    permission_classes = [IsAuthenticated]
    action = 'list'

