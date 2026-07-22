from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect

from applications.models import Application
from opportunities.models import Opportunity
from hours.models import HourLog
from organizations.models import Organization
from volunteers.models import VolunteerProfile
from accounts.decorators import role_required
from accounts.models import User


@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_superuser or user.is_system_admin:
        return redirect("dashboard:admin_dashboard")
    if user.is_org_admin:
        return redirect("dashboard:org_dashboard")
    return redirect("dashboard:volunteer_dashboard")


@role_required("volunteer")
def volunteer_dashboard(request):
    profile, _ = VolunteerProfile.objects.get_or_create(user=request.user)
    applications = Application.objects.filter(volunteer=request.user).select_related("opportunity")[:5]
    recent_hours = HourLog.objects.filter(volunteer=request.user).select_related("opportunity")[:5]
    recommended = Opportunity.objects.filter(status="published").exclude(
        applications__volunteer=request.user
    )[:4]
    return render(request, "dashboard/volunteer_dashboard.html", {
        "profile": profile,
        "applications": applications,
        "recent_hours": recent_hours,
        "recommended": recommended,
        "total_approved_hours": profile.total_approved_hours,
    })


@role_required("org_admin")
def org_dashboard(request):
    org = getattr(request.user, "organization", None)
    if org is None:
        return redirect("organizations:edit")
    opportunities = org.opportunities.all()
    pending_applications = Application.objects.filter(
        opportunity__organization=org, status="pending"
    ).select_related("volunteer", "opportunity")
    pending_hours = HourLog.objects.filter(
        opportunity__organization=org, status="pending"
    ).select_related("volunteer", "opportunity")
    return render(request, "dashboard/org_dashboard.html", {
        "org": org,
        "opportunities": opportunities,
        "pending_applications": pending_applications,
        "pending_hours": pending_hours,
    })


@role_required("admin")
def admin_dashboard(request):
    stats = {
        "total_volunteers": User.objects.filter(role="volunteer").count(),
        "total_organizations": Organization.objects.count(),
        "unverified_organizations": Organization.objects.filter(is_verified=False).count(),
        "total_opportunities": Opportunity.objects.count(),
        "published_opportunities": Opportunity.objects.filter(status="published").count(),
        "total_applications": Application.objects.count(),
        "total_approved_hours": HourLog.objects.filter(status="approved").aggregate(
            total=Sum("hours")
        )["total"] or 0,
    }
    unverified_orgs = Organization.objects.filter(is_verified=False)
    return render(request, "dashboard/admin_dashboard.html", {"stats": stats, "unverified_orgs": unverified_orgs})


@role_required("admin")
def verify_organization(request, pk):
    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    org = get_object_or_404(Organization, pk=pk)
    if request.method == "POST":
        org.is_verified = True
        org.save()
        messages.success(request, f"{org.name} has been verified.")
    return redirect("dashboard:admin_dashboard")
