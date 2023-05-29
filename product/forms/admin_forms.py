from django import forms

from config.common_admin_forms.admin_forms import ImageAdminForm
from product.models import ProductImage


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
