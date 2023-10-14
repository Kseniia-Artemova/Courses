from datetime import timedelta
from typing import Any

import requests
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.reverse import reverse

from config import settings
from courses.models import Course, Payment


def get_payment_link(request: HttpRequest, course: Course) -> tuple[Any, Any]:
    """
    Функция, которая интегрирует функционал
    оплаты со стороннего сервиса stripe.com
    и возвращает ссылку на страницу с оплатой
    """

    get_or_create_product(course)
    price_id = create_price(course)
    course_detail = request.build_absolute_uri(reverse('courses:course_detail',
                                                       kwargs={'pk': course.pk}))

    params = {'line_items[0][price]': price_id,
              'line_items[0][quantity]': 1,
              'success_url': course_detail,
              'cancel_url': course_detail,
              'mode': 'payment',
              }

    response = requests.post(settings.SESSION_URL, headers=settings.HEADERS, params=params).json()
    return response.get('id'), response.get('url')


def get_or_create_product(course: Course) -> str:
    """Вспомогательная функция для создания товара в сервисе stripe.com"""

    if not course.stripe_id:
        params = {'name': course.name}
        response = requests.post(settings.PRODUCT_URL, headers=settings.HEADERS, params=params)
        course.stripe_id = response.json().get('id', None)
        course.save()
    return course.stripe_id


def create_price(course: Course) -> str:
    """Вспомогательная функция для создания цены в сервисе stripe.com"""

    unit_amount_in_kopecks = course.price * 100
    params = {'unit_amount': unit_amount_in_kopecks,
              'currency': 'rub',
              'product': course.stripe_id}
    response = requests.post(settings.PRICE_URL, headers=settings.HEADERS, params=params)
    return response.json().get('id')


def is_payment_succeed(session_id: str) -> str:
    """Функция для проверки успешности платежа"""

    response = requests.get(settings.SESSION_URL + f'/{session_id}', headers=settings.HEADERS)
    return response.json().get('payment_status') == 'paid'


def update_payment_status() -> None:
    """Функция для обновления статуса платежей в случае получения ответа об успешной оплате"""

    one_week = timezone.now() - timedelta(days=7)
    inactive_payments = Payment.objects.filter(date__gt=one_week, is_succeed=False)
    for payment in inactive_payments:
        session_id = payment.id_stripe_session
        if is_payment_succeed(session_id):
            payment.is_succeed = True
            payment.save()
