from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model supporting three roles in the platform."""

    class Role(models.TextChoices):
        VOLUNTEER = "volunteer", "Volunteer"
        ORG_ADMIN = "org_admin", "Organization Admin"
        SYSTEM_ADMIN = "admin", "System Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VOLUNTEER)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_volunteer(self):
        return self.role == self.Role.VOLUNTEER

    @property
    def is_org_admin(self):
        return self.role == self.Role.ORG_ADMIN

    @property
    def is_system_admin(self):
        return self.role == self.Role.SYSTEM_ADMIN or self.is_superuser
