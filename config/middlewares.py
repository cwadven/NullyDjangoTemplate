from django.http import HttpResponseNotAllowed
from django.template import loader


class Handle405Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 405:
            t = loader.get_template('405.html')
            return HttpResponseNotAllowed(t.render(), content_type='text/html')

        return response
