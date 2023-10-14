from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from users import services
from courses.services import subscriptions, payments


@shared_task
def task_send_updates(course_id: int, url: str) -> None:
    """Функция для отправки писем об обновлениях курса"""

    subscriptions.send_updates(course_id, url)


@shared_task
def task_deactivate_users() -> None:
    """
    Блокирует всех пользователей, кроме менеджеров, персонала и суперпользователей,
    если они не заходили в аккаунт более месяца
    """

    services.deactivate_users()


@shared_task
def task_update_payment_status() -> None:
    """Функция для обновления статуса платежей в случае получения ответа об успешной оплате"""

    payments.update_payment_status()
    print('Статусы платежей обновлены!')


ten_sec = IntervalSchedule.objects.create(every=10,
                                          period=IntervalSchedule.SECONDS)

PeriodicTask.objects.create(
    interval=ten_sec,
    name='Update payment statuses',
    task='courses.tasks.task_update_payment_status',
    expires=timezone.now() + timedelta(seconds=30)
)
