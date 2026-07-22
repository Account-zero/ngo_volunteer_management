from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_active", "created_at")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Volunteer Profile Info", {
            "fields": ("role", "phone", "profile_picture", "date_of_birth", "address", "bio")
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Role", {"fields": ("role", "email")}),
    )
