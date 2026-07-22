from django.conf import settings
from django.db import models
from django.urls import reverse

from organizations.models import Organization
from volunteers.models import Skill


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Opportunity(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CLOSED = "closed", "Closed"
        COMPLETED = "completed", "Completed"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="opportunities")
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="opportunities")
    skills_required = models.ManyToManyField(Skill, blank=True, related_name="opportunities")
    location = models.CharField(max_length=255, blank=True)
    is_remote = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    volunteers_needed = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("opportunities:detail", args=[self.pk])

    @property
    def approved_volunteers_count(self):
        return self.applications.filter(status="approved").count()

    @property
    def spots_remaining(self):
        return max(self.volunteers_needed - self.approved_volunteers_count, 0)

    @property
    def is_full(self):
        return self.spots_remaining <= 0
