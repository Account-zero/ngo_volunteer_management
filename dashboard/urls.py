from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_redirect, name="redirect"),
    path("volunteer/", views.volunteer_dashboard, name="volunteer_dashboard"),
    path("organization/", views.org_dashboard, name="org_dashboard"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/verify-org/<int:pk>/", views.verify_organization, name="verify_organization"),
]
