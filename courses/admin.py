from django.contrib import admin

from courses.models import Course, Lesson, Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('id', 'name', 'description', 'user')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    list_display = ('id', 'name', 'description', 'user', 'video')


admin.site.register(Payment)