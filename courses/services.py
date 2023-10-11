import requests
from django.http import HttpRequest
from rest_framework.reverse import reverse

from config import settings
from courses.models import Course


def get_payment_link(request: HttpRequest, object: Course) -> str:
    """
    Функция, которая интегрирует функционал
    оплаты со стороннего сервиса stripe.com
    и возвращает ссылку на страницу с оплатой
    """

    get_or_create_product(object)
    price_id = create_price(object)
    success_url = request.build_absolute_uri(reverse('courses:create_payment', kwargs={'course_pk': object.pk}))

    params = {"line_items[0][price]": price_id,
              "line_items[0][quantity]": 1,
              "after_completion[type]": 'redirect',
              "after_completion[redirect][url]": success_url}
    response = requests.post(settings.URL_PAYMENT_LINK, headers=settings.HEADERS, params=params)
    return response.json().get('url')


def get_or_create_product(object: Course) -> str:
    """Вспомогательная функция для создания товара в сервисе stripe.com"""

    if not object.stripe_id:
        params = {'name': object.name}
        response = requests.post(settings.URL_PRODUCT, headers=settings.HEADERS, params=params)
        object.stripe_id = response.json().get('id', None)
        object.save()
    return object.stripe_id


def create_price(object: Course) -> str:
    """Вспомогательная функция для создания цены в сервисе stripe.com"""

    unit_amount_in_kopecks = object.price * 100
    params = {'unit_amount': unit_amount_in_kopecks,
              'currency': 'rub',
              'product': object.stripe_id}
    response = requests.post(settings.URL_PRICE, headers=settings.HEADERS, params=params)
    return response.json().get('id')

