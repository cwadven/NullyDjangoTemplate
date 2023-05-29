from django.db import models

from config.model_interfaces.common_model_interfaces import DateTimeActiveMixin, CreateModifyTimeMixin


class Banner(DateTimeActiveMixin, CreateModifyTimeMixin):
    description = models.TextField(verbose_name='관리자 보기 위한 설명', blank=True, null=True)
    image = models.TextField(verbose_name='이미지', blank=True, null=True)
    on_click_link = models.TextField(verbose_name='클릭 시 링크', null=True)
    sequence = models.PositiveIntegerField(
        verbose_name='순서',
        default=1,
        help_text='숫자가 작을수록 앞에 있음',
        db_index=True,
    )

    class Meta:
        verbose_name = '배너'
        verbose_name_plural = '배너'

    def __str__(self):
        return f'{self.id} - {self.description}'
