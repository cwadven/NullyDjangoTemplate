from django import forms
from typing import Tuple, List

from common_library import generate_presigned_url, upload_file_to_presigned_url


class ImageAdminForm(forms.ModelForm):
    class Meta:
        abstract = True

    @staticmethod
    def upload_image_files(instance, cleaned_data, image_file_field_set_names: List[Tuple[str, str]]):
        for image_file_field_name, image_char_field_name in image_file_field_set_names:
            if cleaned_data[image_file_field_name]:
                response = generate_presigned_url(
                   cleaned_data[image_file_field_name].name,
                   _type=f'{instance.__class__.__name__}_{image_char_field_name}',
                   unique=str(instance.id) if instance.id else '0'
                )
                upload_file_to_presigned_url(
                    response['url'],
                    response['fields'],
                    cleaned_data[image_file_field_name].file
                )
                setattr(instance, image_char_field_name, response['url'] + response['fields']['key'])


class InlineDataAdminModelForm(forms.ModelForm):
    """
    set_inline_table_fields 를 받아서 해당 필드에 대한 데이터를 세팅합니다.
    attribute 에 세팅해서 사용합니다.

    ex) set_inline_table_fields = ['product_time_info__info_type']
    self.product_time_info__info_type 에 데이터를 세팅합니다.
    """
    class Meta:
        abstract = True

    def _clean_fields(self):
        super()._clean_fields()
        self._set_inline_field_datas(getattr(self.Meta, 'set_inline_table_fields', []))

    def _set_inline_field_datas(self, inline_field_names):
        field_datas = []
        for inline_field_name in inline_field_names:
            try:
                table_name, field_name = inline_field_name.split('__')
                for index in range(int(self.data['{}s-TOTAL_FORMS'.format(table_name)])):
                    if self.data.get('{}s-{}-DELETE'.format(table_name, index)) == 'on':
                        continue
                    field_datas.append(
                        self.data['{}s-{}-{}'.format(table_name, index, field_name)]
                    )
                setattr(self, inline_field_name, field_datas)
            except Exception as e:
                raise AttributeError(
                    f'{self.__class__.__name__} error: {e}'
                )
