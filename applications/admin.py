from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "opportunity", "status", "applied_at", "reviewed_by")
    list_filter = ("status",)
    search_fields = ("volunteer__username", "opportunity__title")
