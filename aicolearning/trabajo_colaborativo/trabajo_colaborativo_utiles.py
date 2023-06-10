# Rutinas útiles para la gestión de la aplicación trabajo_colaborativo

from modelos_de_alumnos import models
from django.shortcuts import get_list_or_404
import time
import threading

# Tipos de agrupamiento aleatorio, homogéneo y heterogéneo
TIPOS_AGRUPAMIENTO = [
        ("aleatorio", "aleatorio"),
        ("homogeneo", "homogeneo"),
        ("heterogeneo", "heterogeneo"),
]

# Obtener las características de un modelo de alumnos a través de su id
def get_caracteristicas_modelo_alumnos(id_modelo_alumnos):
        
        # extrae las lista de características del modelo de alumnos
        
        caracteristicas=get_list_or_404(models.Caracteristica, definicion_modelo_id=id_modelo_alumnos)

        lista_caracteristicas = []
        # recorre las características	
        for caracteristica in caracteristicas:
            # Añade las características a la lista
            #lista_caracteristicas.append((caracteristica.etiqueta))
            lista_caracteristicas.append(caracteristica.etiqueta)

        # Devuelve la lista de características
        return lista_caracteristicas

# Obtener los ids de las características de un modelo de alumnos a través de su id
def get_ids_caracteristicas_modelo_alumnos(id_modelo_alumnos):
        # extrae las lista de características del modelo de alumnos
        
        caracteristicas=get_list_or_404(models.Caracteristica, definicion_modelo_id=id_modelo_alumnos)

        lista_ids_caracteristicas = []
        # recorre las características	
        for caracteristica in caracteristicas:
            # Añade las características a la lista
            #lista_caracteristicas.append((caracteristica.etiqueta))
            lista_ids_caracteristicas.append(caracteristica.id)

        # Devuelve la lista de características
        return lista_ids_caracteristicas             

# Obtener los ids de las características a partir de una lista de etiquetas
def get_ids_caracteristicas(id_modelo_alumnos, etiquetas_caracteristicas):
        # extrae las lista de características del modelo de alumnos
        caracteristicas=get_list_or_404(models.Caracteristica, definicion_modelo_id=id_modelo_alumnos, etiqueta__in=etiquetas_caracteristicas)
        
        lista_ids_caracteristicas = []
        # recorre las características	
        for caracteristica in caracteristicas:
                # Añade las características a la lista
                lista_ids_caracteristicas.append(caracteristica.id)
        
        # Devuelve la lista de características
        return lista_ids_caracteristicas      

# Obtener los ids de los alumnos de un modelo de alumnos
def get_ids_alumnos_modelo(id_modelo_alumnos):
                
        # extrae las lista de alumnos del modelo de alumnos
        #alumnos = models.Alumno.objects.filter(definicion_modelo_id=id_modelo_alumnos)
        
        #alumnos=get_list_or_404(centro_de_estudios_models.Alumno, definicion_modelo_id=id_modelo_alumnos)
        datos_modelo=get_list_or_404(models.DatoModelo, modelo_id=id_modelo_alumnos)
        
        lista_ids_alumnos = []
        
        # recorre las alumnos	
        for dato_modelo in datos_modelo:
                # Añade las ids de los alumnos a la lista
                lista_ids_alumnos.append(dato_modelo.id_alumno)
        
        # Devuelve la lista de ids de los alumnos
        return lista_ids_alumnos

# Clase que lanza el agrupamiento en un thread en segundo plano
class ThreadAgrupar(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        # Simular un proceso largo
        time.sleep(15)
        # Realiza aquí la lógica del proceso largo
