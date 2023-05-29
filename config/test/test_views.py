from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from config.consts import TemplateHtml
from popup.models import HomePopupModal


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.home_popup_modal1 = HomePopupModal.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
            height=100,
            width=100,
        )
        self.home_popup_modal2 = HomePopupModal.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
            height=100,
            width=100,
        )

    def test_home_view_when_cookie_exists_with_modals(self):
        # Given: self.home_popup_modal1 의 Cookie 가 있는 경우
        self.client.cookies.load({f'home_popup_modal_{self.home_popup_modal1.id}': 'true'})

        # When: home view에 GET 요청
        response = self.client.get(reverse('home'))

        # Then: 성공
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, TemplateHtml.HOME.value)
        # And: Modal 이름
        self.assertEqual(response.context['modal_name'], 'home_popup_modal_')
        # And: Cookie 에 없는 Modal 조회
        self.assertEqual(len(response.context['home_popup_modals']), 1)
        self.assertEqual(response.context['home_popup_modals'][0]['id'], self.home_popup_modal2.id)
