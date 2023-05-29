from django.contrib import admin

from custom_account.models import (
    User,
)


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nickname',
        'user_type',
        'user_status',
        'user_provider',
    ]


admin.site.register(User, UserAdmin)
