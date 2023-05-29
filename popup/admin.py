from django.contrib import admin

from popup.forms.admin_forms import HomePopupModalAdminForm
from popup.models import HomePopupModal


class HomePopupModalAdmin(admin.ModelAdmin):
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
    form = HomePopupModalAdminForm


admin.site.register(HomePopupModal, HomePopupModalAdmin)
