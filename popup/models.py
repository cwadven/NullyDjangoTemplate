from django.db import models

from config.model_interfaces.common_model_interfaces import DateTimeActiveMixin, CreateModifyTimeMixin


class Popup(DateTimeActiveMixin, CreateModifyTimeMixin):
    image = models.TextField(verbose_name='이미지', blank=True, null=True)
    description = models.TextField(verbose_name='관리자 보기 위한 설명', blank=True, null=True)
    on_clicK_link = models.TextField(verbose_name='이미지 클릭 시 링크', null=True)
    height = models.PositiveIntegerField(verbose_name='모달 높이')
    width = models.PositiveIntegerField(verbose_name='모달 너비')

    class Meta:
        abstract = True


class HomePopupModal(Popup):
    objects = models.Manager()

    def __str__(self):
        return f'{self.id} - {self.description}'
