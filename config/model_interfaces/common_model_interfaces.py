from django.db import models

from config.common_querysets.common_model_querysets import DateTimeActiveMixinQuerySet


class DateTimeActiveMixin(models.Model):
    start_time = models.DateTimeField(blank=True, null=True, db_index=True)
    end_time = models.DateTimeField(blank=True, null=True, db_index=True)
    is_active = models.BooleanField(default=False, db_index=True)

    datetime_active_objects = DateTimeActiveMixinQuerySet.as_manager()

    class Meta:
        abstract = True


class CreateModifyTimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
