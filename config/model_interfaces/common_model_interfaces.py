from django.db import models

from config.common_querysets.common_model_querysets import DateTimeActiveMixinQuerySet


class DateTimeActiveMixin(models.Model):
    start_time = models.DateTimeField(verbose_name='시작 시간', blank=True, null=True, db_index=True)
    end_time = models.DateTimeField(verbose_name='종료 시간', blank=True, null=True, db_index=True)
    is_active = models.BooleanField(verbose_name='활성화 여부', default=False, db_index=True)

    datetime_active_objects = DateTimeActiveMixinQuerySet.as_manager()

    class Meta:
        abstract = True


class CreateModifyTimeMixin(models.Model):
    created_at = models.DateTimeField(verbose_name='생성 시간', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정 시간', auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(verbose_name='삭제 여부', default=False, db_index=True)

    class Meta:
        abstract = True
