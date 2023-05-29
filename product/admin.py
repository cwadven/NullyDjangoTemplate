from django.contrib import admin

from product.models import ProductType, ProductItemInfoType, Product, ProductItem, ProductImage, ProductItemInfo


class ProductTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProductType, ProductTypeAdmin)


class ProductItemInfoTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProductItemInfoType, ProductItemInfoTypeAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]


admin.site.register(Product, ProductAdmin)


class ProductItemInfoInline(admin.TabularInline):
    model = ProductItemInfo
    extra = 0


class ProductItemAdmin(admin.ModelAdmin):
    inlines = [
        ProductItemInfoInline,
    ]


admin.site.register(ProductItem, ProductItemAdmin)
