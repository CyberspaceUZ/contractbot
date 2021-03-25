from django.contrib import admin
from .models import User
from django.contrib.auth import get_user_model
# Register your models here.

User = get_user_model()
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
     fields = ('phone_number', 'username', 'first_name', 'last_name', 'type', 'organization_name')
     list_display = ('first_name', 'last_name', 'type', 'organization_name')
     list_filter = ('type',)
