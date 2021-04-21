from django.contrib import admin
from app.consultation.models import Consultation


@admin.register(Consultation)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'receiver',
        'territory',
        'status',
    )
    list_filter = (
        'status',
        'territory',
    )
    date_hierarchy = 'created_at'
    exclude = (
        'receiver_msg_id',
        'tg_last_kb',
        'tg_owner_file_id',
        'tg_receiver_file_id',
    )
    readonly_fields = (
        'territory',
        'status',
        'owner',
        'receiver',
        'question',
        'answer',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
