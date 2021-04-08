from django.contrib import admin

from app.account.models import BotUser


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_number',
        'company',
        'occupation',
        'created_at',
    )
    readonly_fields = (
        'full_name',
        'phone_number',
        'company',
        'occupation',
        'created_at',
        'chat_id',
        'created_at',
        'updated_at',
        'language',
    )
    exclude = (
        'is_active',
    )
    ordering = (
        'full_name',
    )
    date_hierarchy = 'created_at'
    search_fields = (
        'phone_number',
        'full_name',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
