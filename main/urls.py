from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path("command/", views.command, name="Command"),
    path("help/", views.help, name="Help"),
    path("admin/", views.admin, name="Admin"),
    path("login/", views.login, name="Login"),
    path("rego/", views.rego, name="Registration"),
]