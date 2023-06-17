from django.shortcuts import render

from product.consts import PRODUCT_DETAIL_HTML
from product.dtos.model_dtos import ProductDetailDTO
from product.services import get_active_product


def get_product_detail(request, product_id):
    product = ProductDetailDTO.of(
        product=get_active_product(product_id)
    ).to_dict()
    return render(request, PRODUCT_DETAIL_HTML, {'product': product})
