from django.contrib import admin
from .models import HourLog


@admin.register(HourLog)
class HourLogAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "opportunity", "date", "hours", "status", "submitted_at")
    list_filter = ("status",)
    search_fields = ("volunteer__username", "opportunity__title")
