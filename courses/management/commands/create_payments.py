import json
from django.core.management import BaseCommand
from config.settings import BASE_DIR
from courses import models
from courses.models import Payment, Course, Lesson


class Command(BaseCommand):

    FILE_NAME = 'payment_data.json'

    def read_json(self):
        file_path = BASE_DIR / self.FILE_NAME
        if file_path.exists() and file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    return json.load(json_file)
            except json.JSONDecodeError as error:
                print(error)

    def handle(self, *args, **options):
        data = self.read_json()

        for payment in data:

            course = payment.get('course')
            lesson = payment.get('lesson')

            Payment.objects.create(
                    client=payment.get('client'),
                    amount=payment.get('amount'),
                    way_pay=payment.get('way_pay'),
                    course=Course.objects.get(pk=course) if course else None,
                    lesson=Lesson.objects.get(pk=lesson) if lesson else None
            )


