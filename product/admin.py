from django.contrib import admin

from product.forms.admin_forms import ProductImageAdminForm, ProductItemAdminForm
from product.models import ProductType, InfoType, Product, ProductItem, ProductImage, ProductItemInfo, ProductInfo


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'sequence',
    ]


admin.site.register(ProductType, ProductTypeAdmin)


class InfoTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]


admin.site.register(InfoType, InfoTypeAdmin)


class ProductInfoInline(admin.TabularInline):
    model = ProductInfo
    extra = 0


class ProductImageInline(admin.TabularInline):
    form = ProductImageAdminForm
    model = ProductImage
    readonly_fields = [
        'image',
    ]
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description',
        'real_price',
        'payment_price',
        'sequence',
        'is_active',
    ]
    readonly_fields = [
        'bought_count',
        'review_count',
        'review_rate',
        'is_deleted',
    ]
    inlines = [
        ProductInfoInline,
        ProductImageInline,
    ]


admin.site.register(Product, ProductAdmin)


class ProductItemInfoInline(admin.TabularInline):
    # Product 에 Info 가 어떻게 됐는지 확인 필요하고 그에 따른 Info 가 전부 있는지 확인해야합니다.
    model = ProductItemInfo
    extra = 0


class ProductItemAdmin(admin.ModelAdmin):
    list_display = [
        'good_number',
        'title',
        'description',
        'additional_payment_price',
        'left_quantity',
        'is_sold_out',
        'is_active',
    ]
    readonly_fields = [
        'bought_count',
        'is_deleted',
    ]
    inlines = [
        ProductItemInfoInline,
    ]
    form = ProductItemAdminForm

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            'product'
        )

        return queryset


admin.site.register(ProductItem, ProductItemAdmin)
