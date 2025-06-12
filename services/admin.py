from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'provider', 'rate', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'rate_type')
    search_fields = ('title', 'description', 'provider__user__username')
