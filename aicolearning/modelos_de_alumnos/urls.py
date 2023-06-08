from django.urls import path

from . import views

app_name = "modelos_de_alumnos"
urlpatterns = [
    # ex: /modelos_de_alumnos/
    #path("", views.index, name="index"),
    path("", views.IndexView.as_view(), name="index"),
    
    # ex: /modelos_de_alumnos/1/
    #path("<int:modelo_id>/", views.modelo, name="modelo"),
    path("<int:pk>/", views.DetailView.as_view(), name="modelo"),

    # ex: /modelos_de_alumnos/importar/
    # Importar datos de alumnos desde un archivo CSV
    path("importar/", views.importar, name="importar"),
]