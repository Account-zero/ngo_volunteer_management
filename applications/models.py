from django.conf import settings
from django.db import models

from opportunities.models import Opportunity


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"
        COMPLETED = "completed", "Completed"

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="applications")
    volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications",
        limit_choices_to={"role": "volunteer"},
    )
    message = models.TextField(blank=True, help_text="Why do you want to volunteer for this opportunity?")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_applications")
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("opportunity", "volunteer")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.volunteer} -> {self.opportunity} ({self.status})"
