import requests
from config import settings


def get_payment_link(object):
    get_or_create_product(object)
    price_id = create_price(object)
    params = {"line_items[0][price]": price_id}
    response = requests.post(settings.URL_PAYMENT_LINK, headers=settings.HEADERS, params=params)
    print(response.json())

    return response.json().get('id')


def get_or_create_product(object):
    if not object.stripe_id:
        params = {'name': object.name}
        response = requests.post(settings.URL_PRODUCT, headers=settings.HEADERS, params=params)
        object.stripe_id = response.json().get('id', None)
        object.save()
        print(response.json())


def create_price(object):
    params = {'unit_amount': object.price,
              'currency': 'rub',
              'product': object.stripe_id}
    response = requests.post(settings.URL_PRICE, headers=settings.HEADERS, params=params)
    return response.json().get('id')

