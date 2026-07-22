from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import HourLog
from .forms import HourLogForm
from accounts.decorators import role_required
from opportunities.models import Opportunity


@role_required("volunteer")
def log_hours(request):
    if request.method == "POST":
        form = HourLogForm(request.POST, volunteer=request.user)
        if form.is_valid():
            hour_log = form.save(commit=False)
            hour_log.volunteer = request.user
            hour_log.save()
            messages.success(request, "Hours submitted for approval.")
            return redirect("hours:my_hours")
    else:
        form = HourLogForm(volunteer=request.user)
    return render(request, "hours/log_hours.html", {"form": form})


@role_required("volunteer")
def my_hours(request):
    logs = HourLog.objects.filter(volunteer=request.user).select_related("opportunity")
    total_approved = sum(l.hours for l in logs if l.status == "approved")
    return render(request, "hours/my_hours.html", {"logs": logs, "total_approved": total_approved})


@role_required("org_admin")
def pending_hours(request):
    logs = HourLog.objects.filter(
        opportunity__organization__admin=request.user, status="pending"
    ).select_related("volunteer", "opportunity")
    return render(request, "hours/pending_hours.html", {"logs": logs})


@role_required("org_admin")
def update_hours_status(request, pk, new_status):
    hour_log = get_object_or_404(HourLog, pk=pk, opportunity__organization__admin=request.user)
    valid_statuses = dict(HourLog.Status.choices)
    if new_status in valid_statuses and request.method == "POST":
        hour_log.status = new_status
        hour_log.approved_by = request.user
        hour_log.approved_at = timezone.now()
        hour_log.save()
        messages.success(request, f"Hours marked as {valid_statuses[new_status]}.")
    return redirect("hours:pending_hours")
