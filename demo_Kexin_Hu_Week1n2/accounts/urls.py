from django.urls import path
from .views import register, dashboard, home

urlpatterns = [
    path("register/", register, name="register"),
    path("dashboard/", dashboard, name="dashboard"),
    path("", home, name="home"),
]
