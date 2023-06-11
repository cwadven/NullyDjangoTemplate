from config.common.exception_codes import ResponseException


class ProductDoesNotExistsException(ResponseException):
    status_code = 400
    default_detail = '유효하지 않은 상품입니다.'
    default_code = 'product-does-not-exists'


class ProductItemDoesNotExistsException(ResponseException):
    status_code = 400
    default_detail = '유효하지 않은 상품 아이템입니다.'
    default_code = 'product-item-does-not-exists'
