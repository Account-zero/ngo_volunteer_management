from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "admin", "email", "is_verified", "created_at")
    list_filter = ("is_verified",)
    search_fields = ("name", "email")
    actions = ["verify_organizations"]

    def verify_organizations(self, request, queryset):
        queryset.update(is_verified=True)
    verify_organizations.short_description = "Mark selected organizations as verified"
