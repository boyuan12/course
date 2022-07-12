from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("day1/", views.day1),
    path("pset1/", views.pset1),
    path("pset2/", views.pset2),
    path("attempt/<int:attempt_id>/", views.view_attempt),
    path("gradebook", views.gradebook),
]