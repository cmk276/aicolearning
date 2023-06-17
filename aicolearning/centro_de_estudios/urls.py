from django.urls import path

from . import views

urlpatterns = [
    path("", views.VistaAlumnos.as_view(), name="alumnos"),
]