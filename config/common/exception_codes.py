class PageSizeMaximumException(Exception):
    status_code = 400
    default_detail = '사이즈를 초과했습니다.'
    default_code = 'page-size-maximum'


class LoginFailedException(Exception):
    status_code = 400
    default_detail = '로그인에 실패했습니다.'
    default_code = 'login-error'


class BlackUserException(Exception):
    status_code = 400
    default_detail = '정지된 유저입니다.'
    default_code = 'inaccessible-user-login'


class DormantUserException(Exception):
    status_code = 400
    default_detail = '휴면상태의 유저입니다.'
    default_code = 'dormant-user-login'


class LeaveUserException(Exception):
    status_code = 400
    default_detail = '탈퇴상태의 유저입니다.'
    default_code = 'leave-user-login'


class UnknownPlatformException(Exception):
    status_code = 400
    default_detail = '알 수 없는 로그인 방식입니다.'
    default_code = 'platform-error'


class UnknownPlatformException(Exception):
    status_code = 400
    default_detail = '알 수 없는 로그인 방식입니다.'
    default_code = 'platform-error'


class MissingMandatoryParameterException(Exception):
    status_code = 400
    default_detail = '입력값을 다시 확인해주세요.'
    default_code = 'missing-mandatory-parameter'
