from django.contrib.auth.models import UserManager

from custom_account.consts import SocialTypeSelector, UserTypeEnum, UserStatusEnum
from custom_account.helpers.social_login_helpers import SocialLoginController


class CustomUserManager(UserManager):
    def get_or_create_user_by_token(self, token: str, provider: int) -> tuple:
        from common_library import generate_random_string_digits

        data = SocialLoginController(
            SocialTypeSelector(int(provider)).selector()
        ).validate(token)

        return self.get_or_create(
            username=data['id'],
            user_provider_id=provider,
            defaults={
                'user_type_id': UserTypeEnum.NORMAL_USER.value,
                'user_status_id': UserStatusEnum.NORMAL_USER.value,
                'email': data['email'] or '',
                'nickname': data['nickname'] or f'Random{generate_random_string_digits(5)}',
            }
        )
