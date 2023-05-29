from io import BytesIO
from PIL import Image
from unittest.mock import Mock, patch

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.utils import timezone

from custom_account.models import User
from popup.forms.admin_forms import HomePopupModalAdminForm
from popup.models import HomePopupModal


class TestHomePopupModalAdminForm(TestCase):
    def setUp(self):
        self.super_user = User.objects.create_superuser(
            username='superuser', password='secret', email='admin@example.com'
        )
        self.client.login(username='superuser', password='secret')
        self.home_popup_modal = HomePopupModal.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
            height=100,
            width=100,
        )
        self.form_data = {
            'description': 'test2',
            'image_file': '',
            'image': '',
            'start_time': timezone.now(),
            'end_time': timezone.now(),
            'height': 300,
            'width': 300,
            'is_active': True,
            '_save': 'Save',
        }
        im = Image.new(mode='RGB', size=(200, 200))
        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)
        self.image = InMemoryUploadedFile(
            im_io, None, 'random-name.jpg', 'image/jpeg', len(im_io.getvalue()), None
        )

    @patch('config.common_admin_forms.admin_forms.upload_file_to_presigned_url', Mock())
    @patch('config.common_admin_forms.admin_forms.generate_presigned_url')
    def test_home_popup_modal_admin_form_success(self, mock_generate_presigned_url):
        # Given: 파일을 생성합니다.
        mock_generate_presigned_url.return_value = {
            'url': 'test',
            'fields': {
                'key': 'test'
            },
        }
        file_form_data = {
            'image_file': self.image,
        }

        # When: form 에 요청했을 경우
        form = HomePopupModalAdminForm(self.form_data, file_form_data)

        # Then: 정상적으로 데이터 생성가능 하도록 True
        self.assertTrue(form.is_valid())
        instance = form.save()

        home_popup_modal = HomePopupModal.objects.get(id=instance.id)
        self.assertEqual(home_popup_modal.description, self.form_data['description'])
        self.assertEqual(home_popup_modal.image, 'testtest')
