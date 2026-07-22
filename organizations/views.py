from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Organization
from .forms import OrganizationForm


def organization_list(request):
    orgs = Organization.objects.filter(is_verified=True)
    paginator = Paginator(orgs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "organizations/organization_list.html", {"page_obj": page_obj})


def organization_detail(request, pk):
    org = get_object_or_404(Organization, pk=pk)
    opportunities = org.opportunities.filter(status="published")
    return render(request, "organizations/organization_detail.html", {
        "org": org, "opportunities": opportunities,
    })


@login_required
def organization_edit(request):
    org = get_object_or_404(Organization, admin=request.user)
    if request.method == "POST":
        form = OrganizationForm(request.POST, request.FILES, instance=org)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization profile updated.")
            return redirect("organizations:detail", pk=org.pk)
    else:
        form = OrganizationForm(instance=org)
    return render(request, "organizations/organization_edit.html", {"form": form, "org": org})
