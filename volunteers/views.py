from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import VolunteerProfile
from .forms import VolunteerProfileForm
from applications.models import Application
from hours.models import HourLog


@login_required
def volunteer_profile_edit(request):
    profile, _ = VolunteerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = VolunteerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Volunteer profile updated.")
            return redirect("volunteers:profile_edit")
    else:
        form = VolunteerProfileForm(instance=profile)
    return render(request, "volunteers/profile_edit.html", {"form": form})


def volunteer_public_profile(request, pk):
    profile = get_object_or_404(VolunteerProfile, user__pk=pk)
    return render(request, "volunteers/profile_detail.html", {"profile": profile})


def volunteer_list(request):
    """For org admins / system admins to browse volunteers."""
    profiles = VolunteerProfile.objects.select_related("user").all()
    paginator = Paginator(profiles, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "volunteers/volunteer_list.html", {"page_obj": page_obj})
