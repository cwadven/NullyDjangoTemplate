from collections import defaultdict

from django.db.models import Q, Count, QuerySet
from typing import List, Tuple

from product.dtos.response_dtos import ProductItemInfoDisplayInformationItemDTO
from product.exception_codes import ProductDoesNotExistsException
from product.models import Product, ProductItem, ProductItemInfo


def get_active_product(product_id: int) -> Product:
    try:
        return Product.datetime_active_objects.get_actives().get(
            id=product_id,
            is_deleted=False,
        )
    except Product.DoesNotExist:
        raise ProductDoesNotExistsException()


def get_active_product_item_filter() -> QuerySet:
    return ProductItem.datetime_active_objects.get_actives().filter(
        is_deleted=False,
    )


def get_product_item_id_by_product_item_info(product_id: int, product_item_infos_information: List[str]) -> QuerySet:
    """
    product_item_infos_information 을 가지고 있는 product_item 의 id 를 가져온다.

    get_product_item_id_by_product_item_info(1, ['빨강', 'S', '물방울'])
    """
    q = Q(product_item_infos__information__in=product_item_infos_information) if product_item_infos_information else Q()
    q2 = Q(distinct_information=len(product_item_infos_information)) if product_item_infos_information else Q()
    return get_active_product_item_filter().filter(
        q,
        product_id=product_id,
    ).values(
        'id',
    ).annotate(
        distinct_information=Count('product_item_infos__information', distinct=True)
    ).filter(
        q2,
    ).values_list(
        'id',
        flat=True,
    )


def get_left_product_item_infos(product_id: int, info_type_id: int, product_item_infos_information: List[str]) -> Tuple[List[str], List[int]]:
    """
    info_type 을 선택하고, 지금까지 선택했던 product_item_info 들로 남은 product_item_info 들을 가져온다.

    get_left_product_item_infos(1, 3, ['빨강', 'S']) --> ['빨강', 'S'] 는 지금까지 선택된 item_infos
    (['물방울'], [1, 2])
    """
    product_item_ids = get_product_item_id_by_product_item_info(product_id, product_item_infos_information)
    q = Q(product_item__id__in=product_item_ids) if product_item_infos_information else Q()

    qs = ProductItemInfo.objects.filter(
        q,
        product_item__product_id=product_id,
        product_item__is_deleted=False,
        info_type_id=info_type_id,
    ).values_list(
        'information',
        'product_item_id',
    ).distinct().order_by(
        'sequence'
    )
    information = []
    product_item_ids = []
    for x in qs:
        if x[0] not in information:
            information.append(x[0])
        if x[1] not in product_item_ids:
            product_item_ids.append(x[1])
    return (
        information,
        product_item_ids,
    )


def get_product_item_info_display_information(information: List[str], product_id: int, product_item_ids: List[int]) -> List[dict]:
    information_by_values = defaultdict(
        lambda: {
            'additional_min_price': None,
            'additional_max_price': None,
            'is_sold_out': True,
            'left_quantity': 0,
        }
    )

    product_item_infos = ProductItemInfo.objects.select_related(
        'product_item'
    ).filter(
        product_item__product_id=product_id,
        information__in=information,
        product_item_id__in=product_item_ids,
    )
    for product_item_info in product_item_infos:
        information = information_by_values[product_item_info.information]
        if information['additional_min_price'] is None:
            information['additional_min_price'] = product_item_info.product_item.additional_payment_price
        else:
            information['additional_min_price'] = min(
                product_item_info.product_item.additional_payment_price,
                information['additional_min_price'],
            )
        if information['additional_max_price'] is None:
            information['additional_max_price'] = product_item_info.product_item.additional_payment_price
        else:
            information['additional_max_price'] = max(
                product_item_info.product_item.additional_payment_price,
                information['additional_max_price']
            )
        information['left_quantity'] += product_item_info.product_item.left_quantity

        information['is_sold_out'] = product_item_info.product_item.is_sold_out and information['is_sold_out']

    return [
        ProductItemInfoDisplayInformationItemDTO(
            information=key,
            additional_min_price=value['additional_min_price'],
            additional_max_price=value['additional_max_price'],
            is_sold_out=value['is_sold_out'],
            left_quantity=value['left_quantity'],
        ).to_dict()
        for key, value in information_by_values.items()
    ]
