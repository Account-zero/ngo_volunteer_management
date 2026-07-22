from django.urls import path
from . import views

app_name = "volunteers"

urlpatterns = [
    path("", views.volunteer_list, name="list"),
    path("profile/edit/", views.volunteer_profile_edit, name="profile_edit"),
    path("<int:pk>/", views.volunteer_public_profile, name="profile_detail"),
]
