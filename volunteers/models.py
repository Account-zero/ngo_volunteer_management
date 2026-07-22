from django.conf import settings
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class VolunteerProfile(models.Model):
    WEEKDAYS = (
        ("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday"),
        ("thu", "Thursday"), ("fri", "Friday"), ("sat", "Saturday"), ("sun", "Sunday"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="volunteer_profile")
    skills = models.ManyToManyField(Skill, blank=True, related_name="volunteers")
    interests = models.TextField(blank=True, help_text="Causes or areas of interest")
    availability_days = models.CharField(max_length=100, blank=True, help_text="Comma-separated day codes, e.g. mon,wed,sat")
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} profile"

    @property
    def total_approved_hours(self):
        from hours.models import HourLog
        total = HourLog.objects.filter(volunteer=self.user, status="approved").aggregate(
            models.Sum("hours")
        )["hours__sum"]
        return total or 0

    @property
    def badge_level(self):
        hours = self.total_approved_hours
        if hours >= 100:
            return "Gold"
        elif hours >= 50:
            return "Silver"
        elif hours >= 10:
            return "Bronze"
        return "New Volunteer"
