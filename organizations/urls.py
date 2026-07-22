from django.urls import path
from . import views

app_name = "organizations"

urlpatterns = [
    path("", views.organization_list, name="list"),
    path("edit/", views.organization_edit, name="edit"),
    path("<int:pk>/", views.organization_detail, name="detail"),
]
