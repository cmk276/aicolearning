from django.urls import path

from . import views

app_name = "trabajo_colaborativo"
urlpatterns = [
    path("", views.index, name="index"),

    # path para la configuración de agrupamiento pasando un número de alumnos por grupo
    # ex /trabajo_colaborativo/configurar_agrupamiento/26/10/2/1,2,3,4,5,6,7,8,9,10
    path("configurar_agrupamiento/<int:id_modelo_alumnos>/<int:num_alumnos>/<int:num_alumnos_por_grupo>/<str:ids_alumnos>", 
         views.VistaConfigurarAgrupamiento.as_view(), name="configurar_agrupamiento"),

    # igual pero sin pasar los ids de alumnos
    path("configurar_agrupamiento/<int:id_modelo_alumnos>/<int:num_alumnos>/<int:num_alumnos_por_grupo>/", 
         views.VistaConfigurarAgrupamiento.as_view(), {'ids_alumnos': ""}, name="configurar_agrupamiento"),

    # Vista temporal para mostrar mientras se calcula el agrupamiento y se muestran los resultados
    # ex /trabajo_colaborativo/temp_agrupando/26/10/aleatorio/1,2,3,4,5,6,7,8,9,10
    path("temp_agrupando/<int:id_modelo_alumnos>/<int:alumnos_por_grupo>/<str:tipo_agrupamiento>/<str:ids_alumnos>",
         views.VistaTempAgrupando.as_view(),
         name="temp_agrupando"),

     # Vista para realizar el agrupamiento
     # ex /trabajo_colaborativo/agrupar/26/10/aleatorio/1,4,5/1,2,3,4,5,6,7
     path("agrupar/<int:id_modelo_alumnos>/<int:alumnos_por_grupo>/<str:tipo_agrupamiento>/<str:ids_caracteristicas>/<str:ids_alumnos>",
          views.VistaAgrupar.as_view(),
          name="agrupar"),

     # Vista para realizar el agrupamiento sin pasar ids de alumnos
     # ex /trabajo_colaborativo/agrupar/26/10/aleatorio/1,4,5/
     path("agrupar/<int:id_modelo_alumnos>/<int:alumnos_por_grupo>/<str:tipo_agrupamiento>/<str:ids_caracteristicas>/",
          views.VistaAgrupar.as_view(),
          {'ids_alumnos': ""},
          name="agrupar"),
]