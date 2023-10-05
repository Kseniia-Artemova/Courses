import re

from rest_framework.exceptions import ValidationError


class LinkValidator:

    def __call__(self, value):
        if not re.match(r'^https://www\.youtube\.com/', value):
            raise ValidationError('Запрещено использовать ссылки на ресурсы, кроме YouTube')