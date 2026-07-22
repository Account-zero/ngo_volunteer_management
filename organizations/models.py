from django.conf import settings
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)
    admin = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organization",
        limit_choices_to={"role": "org_admin"},
    )
    description = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    logo = models.ImageField(upload_to="org_logos/", blank=True, null=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def active_opportunities_count(self):
        return self.opportunities.filter(status="published").count()
