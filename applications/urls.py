from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("apply/<int:pk>/", views.apply_to_opportunity, name="apply"),
    path("mine/", views.my_applications, name="my_applications"),
    path("withdraw/<int:pk>/", views.withdraw_application, name="withdraw"),
    path("review/<int:opportunity_pk>/", views.review_applications, name="review_applications"),
    path("status/<int:pk>/<str:new_status>/", views.update_application_status, name="update_status"),
]
