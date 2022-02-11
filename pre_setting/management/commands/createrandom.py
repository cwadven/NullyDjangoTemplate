import random
from copy import deepcopy

from django.core.management.base import BaseCommand
from django.apps import apps
from django_seed import Seed


class Command(BaseCommand):
    help = "랜덤 데이터 넣는 명령"

    def add_arguments(self, parser):
        # 위치 인자
        parser.add_argument("app_name", type=str, help="앱 명")
        parser.add_argument("model_name", type=str, help="테이블 명")

        # 키워드 인자 (named arguments)
        parser.add_argument('-n', '--number', type=int, help='랜덤 생성 개수', default=1)

    def handle(self, *args, **kwargs):
        """
        실행할 동작을 정의해 줌
        """
        app_name = kwargs.get("app_name")
        model_name = kwargs.get("model_name")
        number = kwargs.get("number")

        seeder = Seed.seeder()

        try:
            model = apps.get_model(app_name, model_name)
            model_fields = model._meta.fields

            foreign_key_seeder_setting = dict()

            # Reference 때문에 이렇게 하나씩 반복 ...
            for _ in range(int(number)):
                for field in model_fields:
                    if field.related_model:
                        _name = field.name
                        _model = field.related_model
                        foreign_key_seeder_setting[_name] = random.choice(_model.objects.all())
                deep_copy = deepcopy(foreign_key_seeder_setting)
                seeder.add_entity(model, 1, deep_copy)
            seeder.execute()

            self.stdout.write(self.style.SUCCESS(f"{app_name} in {model_name} Table Random Data {number} Created"))
        except LookupError as e:
            self.stdout.write(self.style.ERROR(e))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))