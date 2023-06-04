from django.urls import path

from . import views

app_name = "modelos_de_alumnos"
urlpatterns = [
    # ex: /modelos_de_alumnos/
    path("", views.index, name="index"),
    # ex: /modelos_de_alumnos/1/
    path("<int:modelo_id>/", views.modelo, name="modelo"),
    # ex: /modelos_de_alumnos/1/importar
    path("<int:modelo_id>/importar",views.importar, name="importar")
]