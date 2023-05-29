from django.contrib import admin

from product.forms.admin_forms import ProductImageAdminForm
from product.models import ProductType, ProductItemInfoType, Product, ProductItem, ProductImage, ProductItemInfo


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'sequence',
    ]


admin.site.register(ProductType, ProductTypeAdmin)


class ProductItemInfoTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'sequence',
    ]


admin.site.register(ProductItemInfoType, ProductItemInfoTypeAdmin)


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
        ProductImageInline,
    ]


admin.site.register(Product, ProductAdmin)


class ProductItemInfoInline(admin.TabularInline):
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


admin.site.register(ProductItem, ProductItemAdmin)
