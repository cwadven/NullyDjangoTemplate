from django.db.models import Q, Count, QuerySet
from typing import List, Tuple

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


def apply_additional_prices(information: List[str], product_item_ids: List[int]):
    information_by_additional_price = dict(
        ProductItemInfo.objects.filter(
            product_item_id__in=product_item_ids,
        ).values_list(
            'information',
            'product_item__additional_payment_price',
        )
    )
    for index, info in enumerate(information):
        additional_price = information_by_additional_price.get(info, 0)
        if additional_price > 0:
            information[index] = f'{info} (+{additional_price})'
        elif additional_price < 0:
            information[index] = f'{info} ({additional_price})'
    return information
