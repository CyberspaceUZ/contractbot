from django.contrib import admin

from app.application.models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'receiver', 'owner_description', 'status']
    list_filter = ('status',)
    date_hierarchy = 'created_at'
    search_fields = ['id', 'owner', 'receiver']


admin.site.register(Application, ApplicationAdmin)
