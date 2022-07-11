from django.urls import path
from . import views

urlpatterns = [
    path("authorize/", views.github_authorize),
    path("callback", views.github_callback)
]