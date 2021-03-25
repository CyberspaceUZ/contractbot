from django.contrib import admin

from app.account.models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'first_name', 'last_name', 'company', 'occupation', 'created_at']
    readonly_fields = ('created_at', 'updated_at',)
    ordering = ('first_name',)
    date_hierarchy = 'created_at'
    search_fields = ('phone_number', 'first_name', 'last_name', 'company')
    list_per_page = 15


admin.site.register(BotUser, BotUserAdmin)
