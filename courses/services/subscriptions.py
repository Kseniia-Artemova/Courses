from django.core.mail import send_mass_mail

from config import settings
from courses.models import Subscription


def send_updates(course_id: int, url: str) -> None:
    """Функция для отправки писем об обновлениях курса"""

    subscriptions = Subscription.objects.filter(course=course_id).select_related('user', 'course')
    messages = []
    for subscription in subscriptions:
        subject = f'Обновления в курсе {subscription.course.name}!'
        message = f'Посмотрите обновления в курсе! {url}'
        user_email = subscription.user.email
        messages.append((subject, message, settings.EMAIL_HOST_USER, [user_email]))

    result = send_mass_mail(tuple(messages), fail_silently=False)
    print(f'Отправка писем, результат: {result} (отправлено {len(messages)} писем)')