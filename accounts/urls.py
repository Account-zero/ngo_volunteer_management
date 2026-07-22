from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("signup/", views.signup_choice, name="signup_choice"),
    path("signup/volunteer/", views.volunteer_signup, name="signup_volunteer"),
    path("signup/organization/", views.organization_signup, name="signup_organization"),
    path("profile/", views.profile, name="profile"),
    path("password-change/", auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html",
        success_url="/accounts/profile/"
    ), name="password_change"),
]
