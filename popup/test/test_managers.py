from django.utils import timezone

from django.test import TestCase

from popup.models import HomePopupModal


class TestDateTimeActiveMixinQuerySetManager(TestCase):
    def setUp(self):
        # start_time, end_time, is_active 값이 다양한 인스턴스들을 생성합니다.
        self.instance1 = HomePopupModal.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
            height=100,
            width=100,
        )
        self.instance2 = HomePopupModal.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=2),
            end_time=timezone.now() - timezone.timedelta(days=1),
            is_active=True,
            height=100,
            width=100,
        )
        self.instance3 = HomePopupModal.objects.create(
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=2),
            is_active=True,
            height=100,
            width=100,
        )
        self.instance4 = HomePopupModal.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1),
            is_active=False,
            height=100,
            width=100,
        )
        # start_time, end_time 모두 null인 경우
        self.instance5 = HomePopupModal.objects.create(
            start_time=None,
            end_time=None,
            is_active=True,
            height=100,
            width=100,
        )
        # start_time만 null인 경우
        self.instance6 = HomePopupModal.objects.create(
            start_time=None,
            end_time=timezone.now() + timezone.timedelta(days=1),
            is_active=True,
            height=100,
            width=100,
        )
        # end_time만 null인 경우
        self.instance7 = HomePopupModal.objects.create(
            start_time=timezone.now() - timezone.timedelta(days=1),
            end_time=None,
            is_active=True,
            height=100,
            width=100,
        )

    def test_get_actives(self):
        # Given:
        actives = HomePopupModal.datetime_active_objects.get_actives()

        # Expected: 이 인스턴스는 현재 활성화되어 있습니다.
        self.assertIn(self.instance1, actives)
        # And: 이 인스턴스는 현재 비활성화되어 있습니다.
        self.assertNotIn(self.instance2, actives)
        # And: 이 인스턴스는 현재 비활성화되어 있습니다.
        self.assertNotIn(self.instance3, actives)
        # And: 이 인스턴스는 현재 비활성화되어 있습니다.
        self.assertNotIn(self.instance4, actives)
        # And: 이 인스턴스는 현재 활성화되어 있습니다. (start_time, end_time 모두 null)
        self.assertIn(self.instance5, actives)
        # And: 이 인스턴스는 현재 활성화되어 있습니다. (start_time만 null)
        self.assertIn(self.instance6, actives)
        # And: 이 인스턴스는 현재 활성화되어 있습니다. (end_time만 null)
        self.assertIn(self.instance7, actives)
