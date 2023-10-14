from datetime import timedelta

from django.contrib.auth.models import Group
from django.utils import timezone

from users.models import User


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