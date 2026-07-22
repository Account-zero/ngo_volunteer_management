from django.urls import path
from . import views

app_name = "opportunities"

urlpatterns = [
    path("", views.opportunity_list, name="list"),
    path("create/", views.opportunity_create, name="create"),
    path("manage/", views.opportunity_manage_list, name="manage_list"),
    path("<int:pk>/", views.opportunity_detail, name="detail"),
    path("<int:pk>/edit/", views.opportunity_edit, name="edit"),
    path("<int:pk>/delete/", views.opportunity_delete, name="delete"),
]
