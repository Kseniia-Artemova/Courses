from celery import shared_task
from django.core.mail import send_mail

from config import settings
from courses.models import Subscription


@shared_task
def send_updates(course_id, url):
    subscriptions = Subscription.objects.filter(course=course_id)
    for subscription in subscriptions:
        result = send_mail(
            subject=f'Обновления в курсе {subscription.course.name}!',
            message=f'Посмотрите обновления в курсе! {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email]
        )
        print(f'Отправка письма, результат: {result}')
