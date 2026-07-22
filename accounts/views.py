from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import VolunteerSignUpForm, OrganizationSignUpForm, ProfileUpdateForm, BootstrapAuthenticationForm
from volunteers.models import VolunteerProfile
from organizations.models import Organization


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    authentication_form = BootstrapAuthenticationForm


def volunteer_signup(request):
    if request.method == "POST":
        form = VolunteerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            VolunteerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Welcome! Your volunteer account has been created.")
            return redirect("dashboard:redirect")
    else:
        form = VolunteerSignUpForm()
    return render(request, "accounts/signup_volunteer.html", {"form": form})


def organization_signup(request):
    if request.method == "POST":
        form = OrganizationSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Organization.objects.create(
                name=form.cleaned_data["organization_name"],
                admin=user,
                email=form.cleaned_data["email"],
            )
            login(request, user)
            messages.success(request, "Welcome! Your organization account has been created and is pending verification.")
            return redirect("dashboard:redirect")
    else:
        form = OrganizationSignUpForm()
    return render(request, "accounts/signup_organization.html", {"form": form})


def signup_choice(request):
    return render(request, "accounts/signup_choice.html")


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})
