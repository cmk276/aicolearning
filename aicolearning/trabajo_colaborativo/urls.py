from django.urls import path
from .trabajo_colaborativo_utiles import TIPOS_AGRUPAMIENTO

from . import views

app_name = "trabajo_colaborativo"
urlpatterns = [
    path("", views.index, name="index"),

    # path para la configuración de agrupamiento pasando un número de alumnos por grupo
    # ex /trabajo_colaborativo/configurar_agrupamiento/26/10/2/aleatorio/
    path("configurar_agrupamiento/<int:id_modelo_alumnos>/<int:num_alumnos>/<int:num_alumnos_por_grupo>/", 
         views.VistaConfigurarAgrupamiento.as_view(), name="configurar_agrupamiento"),

    path("confirmar_agrupamiento/<int:id_modelo_alumnos>/<int:num_alumnos>/<str:tipo_agrupamiento>",name="confirmar_agrupamiento"),
]