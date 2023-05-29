from django.utils import timezone

from django.db.models import QuerySet, Q


class DateTimeActiveMixinQuerySet(QuerySet):
    def get_actives(self, now=None):
        if now is None:
            now = timezone.now()

        return self.filter(
            (Q(start_time__lte=now) | Q(start_time__isnull=True)),
            (Q(end_time__gte=now) | Q(end_time__isnull=True)),
            is_active=True,
        )
