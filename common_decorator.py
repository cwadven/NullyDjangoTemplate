from functools import wraps
from django.http import HttpRequest

from common_library import optional_key, mandatory_key


def optionals(*keys):
    def decorate(func):
        def wrapper(View, *args, **kwargs):
            optional = dict()
            for arg in keys:
                for key, val in arg.items():
                    data = optional_key(View.request, key, val)
                    optional[key] = data
            return func(View, o=optional, *args, **kwargs)

        return wrapper

    return decorate


def mandatories(*keys):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 첫 번째 인자가 HttpRequest 인스턴스인지 확인
            if isinstance(args[0], HttpRequest):
                request = args[0]
            else:  # 첫 번째 인자가 View 클래스의 인스턴스라고 가정
                request = args[0].request

            mandatory = {key: mandatory_key(request, key) for key in keys}
            kwargs.update(m=mandatory)
            return func(*args, **kwargs)

        return wrapper

    return decorate
