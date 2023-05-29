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
