from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("day1/", views.day1),
    path("day2/", views.day2),
    path("day3/", views.day3),
    path("day4/", views.day4),

    path("pset1/", views.pset1),
    path("pset2/", views.pset2),
    path("pset3/", views.pset3),
    path("pset4/", views.pset4),

    path("attempt/<int:attempt_id>/", views.view_attempt),
    path("gradebook", views.gradebook),
]