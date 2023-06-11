class ResponseException(Exception):
    status_code = 400
    default_detail = '예상치 못한 에러가 발생했습니다.'
    default_code = 'unexpected-error'

    @classmethod
    def to_message(cls):
        return {
            'message': cls.default_detail,
        }


class PageSizeMaximumException(ResponseException):
    status_code = 400
    default_detail = '사이즈를 초과했습니다.'
    default_code = 'page-size-maximum'


class LoginFailedException(ResponseException):
    status_code = 400
    default_detail = '로그인에 실패했습니다.'
    default_code = 'login-error'


class SocialLoginTokenErrorException(ResponseException):
    status_code = 400
    default_detail = '소셜 로그인에 발급된 토큰에 문제가 있습니다.'
    default_code = 'social-token-error'


class BlackUserException(ResponseException):
    status_code = 400
    default_detail = '정지된 유저입니다.'
    default_code = 'inaccessible-user-login'


class DormantUserException(ResponseException):
    status_code = 400
    default_detail = '휴면상태의 유저입니다.'
    default_code = 'dormant-user-login'


class LeaveUserException(ResponseException):
    status_code = 400
    default_detail = '탈퇴상태의 유저입니다.'
    default_code = 'leave-user-login'


class UnknownPlatformException(ResponseException):
    status_code = 400
    default_detail = '알 수 없는 로그인 방식입니다.'
    default_code = 'platform-error'


class UnknownPlatformException(ResponseException):
    status_code = 400
    default_detail = '알 수 없는 로그인 방식입니다.'
    default_code = 'platform-error'


class MissingMandatoryParameterException(ResponseException):
    status_code = 400
    default_detail = '입력값을 다시 확인해주세요.'
    default_code = 'missing-mandatory-parameter'
