from django.urls import path
from . import views

app_name = "hours"

urlpatterns = [
    path("log/", views.log_hours, name="log_hours"),
    path("mine/", views.my_hours, name="my_hours"),
    path("pending/", views.pending_hours, name="pending_hours"),
    path("status/<int:pk>/<str:new_status>/", views.update_hours_status, name="update_status"),
]
