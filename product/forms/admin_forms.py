from django import forms
from django.core.exceptions import ValidationError

from config.common_admin_forms.admin_forms import ImageAdminForm, InlineDataAdminModelForm
from product.models import ProductImage, ProductItem


class ProductImageAdminForm(ImageAdminForm):
    image = forms.CharField(label='image 이미지 주소', required=False)
    image_file = forms.ImageField(label='image 이미지 업로드', required=False)

    class Meta:
        model = ProductImage
        fields = '__all__'

    def save(self, commit=True):
        instance = super(ProductImageAdminForm, self).save(commit=False)
        self.upload_image_files(instance, self.cleaned_data, [('image_file', 'image')])
        if commit:
            instance.save()
        return instance


class ProductItemAdminForm(InlineDataAdminModelForm):
    class Meta:
        model = ProductItem
        fields = '__all__'
        set_inline_table_fields = [
            'product_item_info__info_type'
        ]

    def clean(self):
        product = self.cleaned_data['product']

        if product:
            product_info_info_id_with_name = dict(
                product.product_infos.values_list(
                    'info_type_id',
                    'info_type__name',
                )
            )
            product_info_info_type_ids = set(product_info_info_id_with_name.keys())
        else:
            product_info_info_id_with_name = {}
            product_info_info_type_ids = set()

        invalidate_info_type_names = []
        for product_info_info_type_id in product_info_info_type_ids.difference(set(map(int, self.product_item_info__info_type))):
            invalidate_info_type_names.append(product_info_info_id_with_name[product_info_info_type_id])

        if invalidate_info_type_names:
            raise ValidationError('상품 아이템 디테일 정보에 {} 정보가 필요합니다.'.format(', '.join(invalidate_info_type_names)))
        return self.cleaned_data
