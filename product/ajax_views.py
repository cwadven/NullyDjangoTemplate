import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from product.dtos.model_dtos import ProductItemDTO
from product.dtos.request_dtos import ProductItemInfoInformationRequestDTO
from product.exception_codes import ProductItemDoesNotExistsException
from product.models import ProductItem
from product.services import (
    get_left_product_item_infos,
    get_active_product_item_filter,
    get_product_item_info_display_information,
)


@csrf_exempt
@require_http_methods(['POST'])
def get_product_item_info_information_with_product_item_id(request, product_id):
    if not request.content_type == 'application/json':
        return JsonResponse({'message': 'Invalid content_type'}, status=400)

    try:
        request_data = ProductItemInfoInformationRequestDTO.by_request(json.loads(request.body))
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)

    information, product_item_ids = get_left_product_item_infos(
        product_id, request_data.info_type_id, request_data.product_item_infos_information,
    )
    return JsonResponse(
        {
            'info': get_product_item_info_display_information(information, product_id, product_item_ids),
            'product_item_id': (
                next(iter(product_item_ids), None)
                if request_data.is_last_selection else None
            )
        },
        status=200,
    )


@require_http_methods(['GET'])
def get_product_item_data(request, product_item_id):
    try:
        product_item = ProductItemDTO.of(
            get_active_product_item_filter().get(
                id=product_item_id,
            )
        )
    except ProductItem.DoesNotExist:
        return JsonResponse(
            ProductItemDoesNotExistsException.to_message(),
            status=400,
        )

    return JsonResponse(
        product_item.to_dict(),
        status=200,
    )
