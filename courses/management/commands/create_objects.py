import json
from django.apps import apps
from django.core.management import BaseCommand
from config.settings import BASE_DIR


class Command(BaseCommand):
    """
    Команда для создания объектов из файла.
    Учитывая структуру, предназначена только для небольших объёмов данных.
    Зато универсальная.

    Требуется особая структура JSON-файла:
    [
       {
        "model": "NameModel",
        "field_1": value_1,
        ...
        "field_N": value_N,
        (структура ниже используется при условии что есть ForeignKey поля)
        "fk": [
          {
            "model_field": "fk_field",
            "model_name": "ModelFK",
            "app_label": "name_app_where_fk_model",
            "pk": fk_object_pk
          },
        ],
        ...
        }
    ]
    """

    # Имя файла с данными в JSON-формате
    FILE_NAME = 'data.json'

    def read_json(self) -> list | None:
        """Вспомогательный метод для чтения данных из JSON-файла"""

        file_path = BASE_DIR / self.FILE_NAME
        if file_path.exists() and file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    return json.load(json_file)
            except json.JSONDecodeError as error:
                print(error)

    def handle(self, *args, **options) -> None:
        """
        Метод для записи данных из JSON-файла в базу данных,
        с созданием соответствующих объектов
        """

        data_list = self.read_json()

        all_models = apps.get_models()

        for data in data_list:

            model_name = data.pop('model')
            foreign_keys = data.pop('fk')

            for model in all_models:
                if model.__name__ == model_name:
                    foreign_keys_data = {}
                    for fk in foreign_keys:
                        model_fk = apps.get_model(app_label=fk.get('app_label'),
                                                  model_name=fk.get('model_name'))
                        fk_object = model_fk.objects.get(pk=fk.get('pk'))
                        fk_field = fk.get('model_field')
                        foreign_keys_data.update({fk_field: fk_object})
                    model.objects.create(**foreign_keys_data, **data)


