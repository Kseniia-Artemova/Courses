from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import CourseListAPIView, CourseRetrieveAPIView, CourseCreateAPIView, CourseUpdateAPIView, \
    CourseDestroyAPIView, LessonViewSet, PaymentListAPIView, subscribe_to_updates, pay_course, \
    PaymentRetrieveAPIView

name_app = CoursesConfig.name

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('list/', CourseListAPIView.as_view(), name='courses_list'),
    path('detail/<int:pk>/', CourseRetrieveAPIView.as_view(), name='course_detail'),
    path('create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('update/<int:pk>/', CourseUpdateAPIView.as_view(), name='course_update'),
    path('delete/<int:pk>/', CourseDestroyAPIView.as_view(), name='course_delete'),
    path('payment/list/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_retrieve'),
    path('<int:course_pk>/pay/', pay_course, name='pay_course'),
    path('subscribe/<int:pk>/', subscribe_to_updates, name='subscribe_to_updates')
] + router.urls
