from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("day1/", views.day1),
    path("day2/", views.day2),
    path("day3/", views.day3),
    path("day4/", views.day4),
    path("day5/", views.day5),
    path("day6/", views.day6),
    path("day7/", views.day7),
    path("day8/", views.day8),

    path("pset1/", views.pset1),
    path("pset2/", views.pset2),
    path("pset3/", views.pset3),
    path("pset4/", views.pset4),
    path("pset5/", views.pset5),
    path("pset6/", views.pset6),

    path("attempt/<int:attempt_id>/", views.view_attempt),
    path("gradebook", views.gradebook),
]