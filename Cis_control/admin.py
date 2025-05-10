from django.contrib import admin
from .models import CisControl


@admin.register(CisControl)
class CisControlAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', )
    ordering = ('id',)
