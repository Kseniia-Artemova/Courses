from django.urls import path
from courses.apps import CoursesConfig
from courses.views import CourseListAPIView, CourseRetrieveAPIView, CourseCreateAPIView, CourseUpdateAPIView, \
    CourseDestroyAPIView

name_app = CoursesConfig.name

urlpatterns = [
    path('courses/list/', CourseListAPIView.as_view(), name='courses_list'),
    path('courses/detail/<int:pk>/', CourseRetrieveAPIView.as_view(), name='course_detail'),
    path('courses/create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('courses/update/<int:pk>/', CourseUpdateAPIView.as_view(), name='course_update'),
    path('courses/delete/<int:pk>/', CourseDestroyAPIView.as_view(), name='course_delete'),
]