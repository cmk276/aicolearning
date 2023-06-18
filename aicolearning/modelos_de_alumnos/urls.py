from django.urls import path

from . import views

app_name = "modelos_de_alumnos"
urlpatterns = [
    # ex: /modelos_de_alumnos/
    path("", views.VistaModelos.as_view(), name="modelos"),
    
    # Muestra los datos de un modelo de alumnos
    # ex: /modelos_de_alumnos/5/
    path("<int:id_modelo>/", views.VistaModelo.as_view(), name="vista_modelo"),

    # ex: /modelos_de_alumnos/importar/
    # Importar datos de alumnos desde un archivo CSV
    path("importar/", views.importar, name="importar"),
]