from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.home, name="Home"),
    path("command/", views.command, name="Command"),
    path("visual/", views.visual, name="Visual"),
    path("help/", views.help, name="Help"),
    path("admin/", views.admin, name="Admin"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
