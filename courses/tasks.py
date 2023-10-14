from datetime import timedelta

from celery import shared_task
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from courses.models import Subscription
from users.models import User


@shared_task
def send_updates(course_id: int, url: str) -> None:
    """Функция для отправки писем об обновлениях курса"""

    subscriptions = Subscription.objects.filter(course=course_id)
    for subscription in subscriptions:
        result = send_mail(
            subject=f'Обновления в курсе {subscription.course.name}!',
            message=f'Посмотрите обновления в курсе! {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email]
        )
        print(f'Отправка письма, результат: {result}')


@shared_task
def deactivate_users() -> None:
    """
    Блокирует всех пользователей, кроме менеджеров, персонала и суперпользователей,
    если они не заходили в аккаунт более месяца
    """

    one_month = timezone.now() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=one_month)
    managers = Group.objects.get(name="Managers")
    regular_users = users.exclude(groups=managers).exclude(is_staff=True).exclude(is_superuser=True)
    regular_users.update(is_active=False)
    print('Неактивные пользователи заблокированы')
