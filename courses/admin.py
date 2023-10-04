from django.contrib import admin

from courses.models import Course, Lesson, Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('id', 'name', 'description', 'user')


admin.site.register(Lesson)
admin.site.register(Payment)