from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """Admin interface for TODO model."""
    list_display = ['title', 'priority', 'due_date', 'is_resolved', 'created_at']
    list_filter = ['is_resolved', 'priority', 'due_date', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_resolved']
    date_hierarchy = 'created_at'
    ordering = ['is_resolved', '-priority', 'due_date']
