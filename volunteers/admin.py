from django.contrib import admin
from .models import Skill, VolunteerProfile


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "badge_level", "total_approved_hours")
    filter_horizontal = ("skills",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
