# Rutinas útiles para la gestión de la aplicación trabajo_colaborativo

from modelos_de_alumnos import models
from django.shortcuts import get_list_or_404

# Tipos de agrupamiento aleatorio, homogéneo y heterogéneo
TIPOS_AGRUPAMIENTO = [
        ("aleatorio", "aleatorio"),
        ("homogeneo", "homogeneo"),
        ("heterogeneo", "heterogeneo"),
]

# Obtener las características de un modelo de alumnos a través de su id
def get_caracteristicas_modelo_alumnos(id_modelo_alumnos):
        
        # extrae las lista de características del modelo de alumnos
        #caracteristicas = models.Caracteristica.objects.filter(definicion_modelo_id=id_modelo_alumnos)

        caracteristicas=get_list_or_404(models.Caracteristica, definicion_modelo_id=id_modelo_alumnos)

        lista_caracteristicas = []
        # recorre las características	
        for caracteristica in caracteristicas:
            # Añade las características a la lista
            #lista_caracteristicas.append((caracteristica.etiqueta))
            lista_caracteristicas.append(caracteristica.etiqueta)

        # Devuelve la lista de características
        return lista_caracteristicas