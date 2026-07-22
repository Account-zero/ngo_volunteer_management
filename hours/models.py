from django.conf import settings
from django.db import models

from opportunities.models import Opportunity


class HourLog(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hour_logs",
        limit_choices_to={"role": "volunteer"},
    )
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="hour_logs")
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_hour_logs")
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.volunteer} - {self.hours}h on {self.date} ({self.status})"
