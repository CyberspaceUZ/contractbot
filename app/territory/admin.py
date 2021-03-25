from django.contrib import admin
from .models import Territory
# Register your models here.


@admin.register(Territory)
class TerritoryAdmin(admin.ModelAdmin):
    list_display = ('name',)