from django.contrib import admin

from banner.forms.admin_forms import BannerAdminForm
from banner.models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'description',
        'on_click_link',
        'sequence',
        'start_time',
        'end_time',
        'is_active',
    ]
    readonly_fields = [
        'image',
    ]
    form = BannerAdminForm


admin.site.register(Banner, BannerAdmin)
