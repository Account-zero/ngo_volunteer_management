from django.contrib import admin
from .models import Category, Opportunity


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "category", "status", "start_date", "end_date", "volunteers_needed")
    list_filter = ("status", "category", "is_remote")
    search_fields = ("title", "description", "organization__name")
    filter_horizontal = ("skills_required",)
