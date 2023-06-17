from django.urls import path

from product.ajax_views import get_product_item_info_information_with_product_item_id, get_product_item_data
from product.views import get_product_detail

app_name = 'product'


urlpatterns = [
    path('<int:product_id>/', get_product_detail, name='get_product'),

    # Ajax
    path(
        '<int:product_id>/product_item_info_information/',
        get_product_item_info_information_with_product_item_id,
        name='get_product_item_info_information_with_product_item_id'
    ),
    path(
        'product_item_info_information/<int:product_item_id>/',
        get_product_item_data,
        name='get_product_item_data'
    )
]
