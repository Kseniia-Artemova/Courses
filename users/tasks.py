from celery import shared_task

from users import services


@shared_task
def task_deactivate_users() -> None:
    """
    Блокирует всех пользователей, кроме менеджеров, персонала и суперпользователей,
    если они не заходили в аккаунт более месяца
    """

    services.deactivate_users()
    print('Неактивные пользователи заблокированы')
