from django.urls import path

from . import views

app_name = "trabajo_colaborativo"
urlpatterns = [
    path("", views.index, name="index"),

    # Vista de agrupamientos
    path("agrupamientos/", views.VistaAgrupamientos.as_view(), name="agrupamientos"),

    # path para la configuración de agrupamiento pasando un número de alumnos por grupo
    # ex /trabajo_colaborativo/configurar_agrupamiento/26/10/2/1,2,3,4,5,6,7,8,9,10
    path("configurar_agrupamiento/<int:id_modelo_alumnos>/<int:num_alumnos>/<int:num_alumnos_por_grupo>/<str:ids_alumnos>", 
         views.VistaConfigurarAgrupamiento.as_view(), name="configurar_agrupamiento"),

    # igual pero sin pasar los ids de alumnos
    path("configurar_agrupamiento/<int:id_modelo_alumnos>/<int:num_alumnos>/<int:num_alumnos_por_grupo>/", 
         views.VistaConfigurarAgrupamiento.as_view(), {'ids_alumnos': ""}, name="configurar_agrupamiento"),

     # Vista para realizar el agrupamiento
     # ex /trabajo_colaborativo/agrupar/26/10/aleatorio/1,4,5/1,2,3,4,5,6,7
     path("agrupar/<int:id_modelo_alumnos>/<int:alumnos_por_grupo>/<str:tipo_agrupamiento>/<str:nombre_agrupamiento>/<str:ids_caracteristicas>/<str:ids_alumnos>",
          views.VistaAgrupar.as_view(),
          name="agrupar"),

     # Vista para realizar el agrupamiento sin pasar ids de alumnos
     # ex /trabajo_colaborativo/agrupar/26/10/aleatorio/1,4,5/
     path("agrupar/<int:id_modelo_alumnos>/<int:alumnos_por_grupo>/<str:tipo_agrupamiento>/<str:nombre_agrupamiento>/<str:ids_caracteristicas>/",
          views.VistaAgrupar.as_view(),
          {'ids_alumnos': ""},
          name="agrupar"),

     # Vista para ver un equipo
     # ex /trabajo_colaborativo/ver_equipo/1/1/1,2,3
     path ("ver_equipo/<int:id_agrupamiento>/<int:id_equipo>/<int:mostrar_info>/<str:ids_caracteristicas>/", 
           views.VistaEquipo.as_view(), name="ver_equipo"),
     # La misma vista sin ids de características
     path ("ver_equipo/<int:id_agrupamiento>/<int:id_equipo>/<int:mostrar_info>/", 
           views.VistaEquipo.as_view(), 
           {'ids_caracteristicas': ""},
           name="ver_equipo"),
     
     # Vista para ver un listado de equipos de un agrupamiento
     path ("ver_equipos/<int:id_agrupamiento>/<int:mostrar_info>/<str:ids_caracteristicas>/",
           views.VistaEquipos.as_view(), name="ver_equipos"),
     # La misma vista sin ids de características
     path ("ver_equipos/<int:id_agrupamiento>/<int:mostrar_info>/",
           views.VistaEquipos.as_view(), 
           {'ids_caracteristicas': ""},
           name="ver_equipos"),

      # Vista para eliminar un agrupamiento -> Elimina un agrupamiento y vuelve a la vista de agrupamientos
      path ("eliminar_agrupamiento/<int:id_agrupamiento>/",
            views.VistaEliminarAgrupamiento.as_view(), name="eliminar_agrupamiento"),

      # Vista para exportar a un fichero csv los datos de un agrupamiento
      path ("exportar_agrupamiento/<int:id_agrupamiento>/",
            views.VistaExportarAgrupamiento.as_view(), name="exportar_agrupamiento"),
            
        
]