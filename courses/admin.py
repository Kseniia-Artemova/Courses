from django.contrib import admin

from courses.models import Course, Lesson, Payment

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Payment)