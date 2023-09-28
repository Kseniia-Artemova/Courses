from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import CourseListAPIView, CourseRetrieveAPIView, CourseCreateAPIView, CourseUpdateAPIView, \
    CourseDestroyAPIView, LessonViewSet, PaymentListAPIView

name_app = CoursesConfig.name

router = DefaultRouter()
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('courses/list/', CourseListAPIView.as_view(), name='courses_list'),
    path('courses/detail/<int:pk>/', CourseRetrieveAPIView.as_view(), name='course_detail'),
    path('courses/create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('courses/update/<int:pk>/', CourseUpdateAPIView.as_view(), name='course_update'),
    path('courses/delete/<int:pk>/', CourseDestroyAPIView.as_view(), name='course_delete'),
    path('payment/list/', PaymentListAPIView.as_view(), name='payment_list')
] + router.urls
