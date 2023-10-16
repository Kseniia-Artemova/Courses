from django.contrib import admin

from courses.models import Course, Lesson, Payment, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('id', 'name', 'description', 'user', 'last_update')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    list_display = ('id', 'name', 'description', 'user', 'video')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = ('id', 'user', 'course')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ('id', 'date', 'amount', 'way_pay', 'id_stripe_session', 'is_succeed', 'user', 'course')
