from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views import View

from account.helpers.payload_validator_helpers import SignUpPayloadValidator
from account.models import User

from common_decorator import mandatories
from common_library import generate_dict_value_by_key_to_cache, get_cache_value_by_key, generate_random_string_digits, \
    delete_cache_value_by_key, increase_cache_int_value_by_key
from .consts import UserCreationExceptionMessage, UserTypeEnum, UserProviderEnum, SIGNUP_MACRO_VALIDATION_KEY, \
    SIGNUP_MACRO_COUNT
from .services import is_username_exists, is_email_exists, is_nickname_exists
from .task import send_one_time_token_email


class SocialLoginView(View):
    @mandatories('provider', 'token')
    def post(self, request, m):
        user, is_created = User.objects.get_or_create_user_by_token(m['token'], m['provider'])
        user.raise_if_inaccessible()

        login(request, user)

        return JsonResponse({})


@mandatories('username', 'password')
def normal_login(request, m):
    user = authenticate(request, username=m['username'], password=m['password'])
    if not user:
        return JsonResponse({'message': '아이디/비밀번호 정보가 일치하지 않습니다.'}, status=400)

    login(request, user)
    return JsonResponse({}, status=200)


class SignUpValidationView(View):
    @mandatories('username', 'email', 'nickname', 'password1', 'password2')
    def post(self, request, m):
        payload_validator = SignUpPayloadValidator(m)
        try:
            payload_validator.validate()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=400)
        return JsonResponse({'result': 'success'}, status=200)


class SignUpEmailTokenSendView(View):
    @mandatories('email', 'username', 'nickname', 'password2')
    def post(self, request, m):
        generate_dict_value_by_key_to_cache(
            key=m['email'],
            value={
                'one_time_token': generate_random_string_digits(),
                'email': m['email'],
                'username': m['username'],
                'nickname': m['nickname'],
                'password2': m['password2'],
            },
            expire_seconds=60 * 2
        )
        value = get_cache_value_by_key(m['email'])
        if value:
            send_one_time_token_email.apply_async(
                (
                    m['email'],
                    value['one_time_token'],
                )
            )
        return JsonResponse({'message': '인증번호를 이메일로 전송했습니다.'}, status=200)


class SignUpEmailTokenValidationEndView(View):
    @mandatories('email', 'one_time_token')
    def post(self, request, m):
        macro_count = increase_cache_int_value_by_key(
            key=SIGNUP_MACRO_VALIDATION_KEY.format(m['email']),
        )
        if macro_count >= SIGNUP_MACRO_COUNT:
            return JsonResponse(
                data={
                    'message': '{}회 이상 인증번호를 틀리셨습니다. 현 이메일은 {}시간 동안 인증할 수 없습니다.'.format(
                        SIGNUP_MACRO_COUNT,
                        24
                    )
                },
                status=400,
            )

        value = get_cache_value_by_key(m['email'])

        if not value:
            return JsonResponse({'message': '이메일 인증번호를 다시 요청하세요.'}, status=400)

        if not value.get('one_time_token') or value.get('one_time_token') != m['one_time_token']:
            return JsonResponse({'message': '인증번호가 다릅니다.'}, status=400)

        # 회원 가입 제약을 위해 더블 체킹 validation
        if is_username_exists(value['username']):
            return JsonResponse({'message': UserCreationExceptionMessage.USERNAME_EXISTS.label}, status=400)
        if is_nickname_exists(value['nickname']):
            return JsonResponse({'message': UserCreationExceptionMessage.NICKNAME_EXISTS.label}, status=400)
        if is_email_exists(value['email']):
            return JsonResponse({'message': UserCreationExceptionMessage.EMAIL_EXISTS.label}, status=400)

        User.objects.create_user(
            username=value['username'],
            nickname=value['nickname'],
            email=value['email'],
            user_type_id=UserTypeEnum.NORMAL_USER.value,
            password=value['password2'],
            user_provider_id=UserProviderEnum.EMAIL.value,
        )

        # 캐시 서버 기록 삭제 (메크로 및 정보 보존용)
        delete_cache_value_by_key(value['email'])
        delete_cache_value_by_key(SIGNUP_MACRO_VALIDATION_KEY.format(m['email']))
        return JsonResponse({'message': f'회원가입에 성공했습니다.'}, status=200)
