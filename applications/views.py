from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Application
from .forms import ApplicationForm
from accounts.decorators import role_required
from opportunities.models import Opportunity


@role_required("volunteer")
def apply_to_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, status="published")
    if opportunity.is_full:
        messages.warning(request, "Sorry, this opportunity is already full.")
        return redirect("opportunities:detail", pk=pk)
    if Application.objects.filter(opportunity=opportunity, volunteer=request.user).exists():
        messages.info(request, "You've already applied to this opportunity.")
        return redirect("opportunities:detail", pk=pk)

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.opportunity = opportunity
            application.volunteer = request.user
            application.save()
            messages.success(request, "Application submitted!")
            return redirect("dashboard:volunteer_dashboard")
    else:
        form = ApplicationForm()
    return render(request, "applications/application_form.html", {"form": form, "opportunity": opportunity})


@role_required("volunteer")
def my_applications(request):
    applications = Application.objects.filter(volunteer=request.user).select_related("opportunity")
    return render(request, "applications/my_applications.html", {"applications": applications})


@role_required("volunteer")
def withdraw_application(request, pk):
    application = get_object_or_404(Application, pk=pk, volunteer=request.user)
    if request.method == "POST":
        application.status = Application.Status.WITHDRAWN
        application.save()
        messages.success(request, "Application withdrawn.")
    return redirect("applications:my_applications")


@role_required("org_admin")
def review_applications(request, opportunity_pk):
    opportunity = get_object_or_404(Opportunity, pk=opportunity_pk, organization__admin=request.user)
    applications = opportunity.applications.select_related("volunteer").all()
    return render(request, "applications/review_applications.html", {
        "opportunity": opportunity, "applications": applications,
    })


@role_required("org_admin")
def update_application_status(request, pk, new_status):
    application = get_object_or_404(Application, pk=pk, opportunity__organization__admin=request.user)
    valid_statuses = dict(Application.Status.choices)
    if new_status in valid_statuses and request.method == "POST":
        application.status = new_status
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save()
        messages.success(request, f"Application marked as {valid_statuses[new_status]}.")
    return redirect("applications:review_applications", opportunity_pk=application.opportunity_id)
