from django.contrib import admin

from app.application.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'owner_description',
        'id',
        'owner',
        'receiver',
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
        'owner_file',
        'owner_description',
        'receiver',
        'receiver_file',
        'receiver_description',

        'contr_agent',
        'agreement_number',
        'date_of_origin',
        'maturity_date',
        'amount',
        'currency',
        'title',
        'covenants',
        'agreement',
        'performance',
        'payment_terms',
        'transfer_risk',
        'inco_terms',

    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
