from django.contrib.auth import login
from django.http import HttpResponse
from django.views import View

from account.models import User

from common_decorator import mandatories


class SocialLoginView(View):
    @mandatories('provider', 'token')
    def post(self, request, m):
        user, is_created = User.objects.get_or_create_user_by_token(m['token'], m['provider'])
        user.raise_if_inaccessible()

        login(request, user)

        return HttpResponse({})
