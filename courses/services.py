from typing import Any

import requests
from django.http import HttpRequest
from rest_framework.reverse import reverse

from config import settings
from courses import serializers
from courses.models import Course


def get_payment_link(request: HttpRequest, object: Course, payment_pk: int) -> tuple[Any, Any]:
    """
    Функция, которая интегрирует функционал
    оплаты со стороннего сервиса stripe.com
    и возвращает ссылку на страницу с оплатой
    """

    get_or_create_product(object)
    price_id = create_price(object)
    success_url = request.build_absolute_uri(reverse('courses:check_payment',
                                                     kwargs={'payment_pk': payment_pk}))
    cancel_url = request.build_absolute_uri(reverse('courses:courses_list'))

    params = {'line_items[0][price]': price_id,
              'line_items[0][quantity]': 1,
              'success_url': success_url,
              'cancel_url': cancel_url,
              'mode': 'payment',
              }

    response = requests.post(settings.SESSION_URL, headers=settings.HEADERS, params=params).json()
    return response.get('id'), response.get('url')


def get_or_create_product(object: Course) -> str:
    """Вспомогательная функция для создания товара в сервисе stripe.com"""

    if not object.stripe_id:
        params = {'name': object.name}
        response = requests.post(settings.PRODUCT_URL, headers=settings.HEADERS, params=params)
        object.stripe_id = response.json().get('id', None)
        object.save()
    return object.stripe_id


def create_price(object: Course) -> str:
    """Вспомогательная функция для создания цены в сервисе stripe.com"""

    unit_amount_in_kopecks = object.price * 100
    params = {'unit_amount': unit_amount_in_kopecks,
              'currency': 'rub',
              'product': object.stripe_id}
    response = requests.post(settings.PRICE_URL, headers=settings.HEADERS, params=params)
    return response.json().get('id')


def check_payment(session_id):
    response = requests.get(settings.SESSION_URL + f'/{session_id}', headers=settings.HEADERS)
    return response.json().get('payment_status')