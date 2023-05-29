from django import forms

from config.common_admin_forms.admin_forms import ImageAdminForm
from banner.models import Banner


class BannerAdminForm(ImageAdminForm):
    description = forms.CharField(label='관리자 보기 위한 설명', required=False)
    on_click_link = forms.CharField(label='이미지 클릭 시 링크', required=False)
    image_file = forms.ImageField(label='image 이미지 업로드', required=False)
    image = forms.CharField(label='image 이미지 주소', required=False)

    class Meta:
        model = Banner
        fields = '__all__'

    def save(self, commit=True):
        instance = super(BannerAdminForm, self).save(commit=False)
        self.upload_image_files(instance, self.cleaned_data, [('image_file', 'image')])
        if commit:
            instance.save()
        return instance
