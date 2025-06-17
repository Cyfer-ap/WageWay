from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewed_user', 'job', 'review_type', 'rating', 'created_at')
    list_filter = ('review_type', 'created_at')
    search_fields = ('reviewer__username', 'reviewed_user__username', 'job__title')
