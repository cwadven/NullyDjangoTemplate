import attr
from typing import List, Tuple

from product.models import Product, ProductItem


@attr.s
class ProductDetailDTO(object):
    id = attr.ib(type=int)
    title = attr.ib(type=str)
    description = attr.ib(type=str)
    real_price = attr.ib(type=int)
    payment_price = attr.ib(type=int)
    bought_count = attr.ib(type=int)
    review_count = attr.ib(type=int)
    review_rate = attr.ib(type=float)
    product_type_names = attr.ib(type=List[str])

    info_types = attr.ib(type=List[dict])
    product_images = attr.ib(type=List[str])

    @classmethod
    def of(cls, product: Product) -> 'ProductDetailDTO':
        return cls(
            id=product.id,
            title=product.title,
            description=product.description,
            real_price=product.real_price,
            payment_price=product.payment_price,
            bought_count=product.bought_count,
            review_count=product.review_count,
            review_rate=product.review_rate,
            product_type_names=list(product.product_type.order_by('sequence').values_list('name', flat=True)),
            product_images=list(product.images.all().order_by('sequence').values_list('image', flat=True)),
            info_types=list(product.product_infos.order_by('sequence').values('info_type_id', 'info_type__name')),
        )

    def to_dict(self):
        return attr.asdict(self, recurse=True)


# Ajax 로 호출 하기
@attr.s
class ProductItemDTO(object):
    id = attr.ib(type=int)
    good_number = attr.ib(type=str)
    title = attr.ib(type=str)
    additional_payment_price = attr.ib(type=int)
    left_quantity = attr.ib(type=int)
    is_sold_out = attr.ib(type=bool)
    total_payment_price = attr.ib(type=int)

    @classmethod
    def of(cls, product_item: ProductItem) -> 'ProductItemDTO':
        return cls(
            id=product_item.id,
            title=product_item.title,
            additional_payment_price=product_item.additional_payment_price,
            good_number=product_item.good_number,
            left_quantity=product_item.left_quantity,
            is_sold_out=product_item.is_sold_out,
            total_payment_price=product_item.product.payment_price + product_item.additional_payment_price,
        )

    def to_dict(self):
        return attr.asdict(self, recurse=True)
