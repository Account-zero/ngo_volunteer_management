from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Opportunity
from .forms import OpportunityForm, OpportunityFilterForm
from accounts.decorators import role_required
from applications.models import Application


def opportunity_list(request):
    opportunities = Opportunity.objects.filter(status="published").select_related("organization", "category")
    form = OpportunityFilterForm(request.GET or None)

    if form.is_valid():
        q = form.cleaned_data.get("q")
        category = form.cleaned_data.get("category")
        is_remote = form.cleaned_data.get("is_remote")
        if q:
            opportunities = opportunities.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            opportunities = opportunities.filter(category=category)
        if is_remote:
            opportunities = opportunities.filter(is_remote=(is_remote == "1"))

    paginator = Paginator(opportunities, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "opportunities/opportunity_list.html", {"page_obj": page_obj, "form": form})


def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    already_applied = False
    if request.user.is_authenticated and request.user.is_volunteer:
        already_applied = Application.objects.filter(opportunity=opportunity, volunteer=request.user).exists()
    return render(request, "opportunities/opportunity_detail.html", {
        "opportunity": opportunity, "already_applied": already_applied,
    })


@role_required("org_admin")
def opportunity_create(request):
    org = request.user.organization
    if request.method == "POST":
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.organization = org
            opportunity.created_by = request.user
            opportunity.save()
            form.save_m2m()
            messages.success(request, "Opportunity created successfully.")
            return redirect("opportunities:detail", pk=opportunity.pk)
    else:
        form = OpportunityForm()
    return render(request, "opportunities/opportunity_form.html", {"form": form, "title": "Create Opportunity"})


@role_required("org_admin")
def opportunity_edit(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, organization__admin=request.user)
    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            messages.success(request, "Opportunity updated.")
            return redirect("opportunities:detail", pk=opportunity.pk)
    else:
        form = OpportunityForm(instance=opportunity)
    return render(request, "opportunities/opportunity_form.html", {"form": form, "title": "Edit Opportunity"})


@role_required("org_admin")
def opportunity_delete(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, organization__admin=request.user)
    if request.method == "POST":
        opportunity.delete()
        messages.success(request, "Opportunity deleted.")
        return redirect("dashboard:redirect")
    return render(request, "opportunities/opportunity_confirm_delete.html", {"opportunity": opportunity})


@role_required("org_admin")
def opportunity_manage_list(request):
    opportunities = Opportunity.objects.filter(organization__admin=request.user)
    return render(request, "opportunities/opportunity_manage_list.html", {"opportunities": opportunities})
