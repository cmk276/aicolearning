# Rutinas útiles para la gestión de la aplicación trabajo_colaborativo

from django.db import models
from modelos_de_alumnos import models as mda_models
from centro_de_estudios import models as cde_models
from trabajo_colaborativo import models as tc_models
from django.shortcuts import get_list_or_404, get_object_or_404
import time
import threading
import numpy as np 
import pandas as pd
from pandas.api.types import CategoricalDtype
import json
import trabajo_colaborativo.teammaker as teammaker


# Tipos de agrupamiento aleatorio, homogéneo y heterogéneo
TIPOS_AGRUPAMIENTO = [
        ("aleatorio", "aleatorio"),
        ("homogeneo", "homogeneo"),
        ("heterogeneo", "heterogeneo"),
]

# Obtener las características de un modelo de alumnos a través de su id
def get_caracteristicas_modelo_alumnos(id_modelo_alumnos):
        
        # extrae las lista de características del modelo de alumnos

        print("Voy a extraer las caracrerísticas de id_modelo_alumnos: ", id_modelo_alumnos)
        
        caracteristicas=get_list_or_404(mda_models.Caracteristica, definicion_modelo_id=id_modelo_alumnos)

        print ("Características: ", caracteristicas)

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

# Obtener las etiquetas de las características a partir de una lista de ids de características
def get_etiquetas_caracteristicas(id_modelo_alumnos, ids_caracteristicas):
        # extrae las lista de características del modelo de alumnos
        caracteristicas=get_list_or_404(mda_models.Caracteristica, definicion_modelo_id=id_modelo_alumnos, id__in=ids_caracteristicas)
        
        lista_etiquetas_caracteristicas = []
        # recorre las características	
        for caracteristica in caracteristicas:
                # Añade las características a la lista
                lista_etiquetas_caracteristicas.append(caracteristica.etiqueta)
        
        # Devuelve la lista de características
        return lista_etiquetas_caracteristicas

# Obtener los ids de los alumnos de un modelo de alumnos
def get_ids_alumnos_modelo(id_modelo_alumnos):
                
        # extrae las lista de alumnos del modelo de alumnos
        #alumnos = models.Alumno.objects.filter(definicion_modelo_id=id_modelo_alumnos)
        
        #alumnos=get_list_or_404(centro_de_estudios_models.Alumno, definicion_modelo_id=id_modelo_alumnos)
        datos_modelo=get_list_or_404(mda_models.DatoModelo, modelo_id=id_modelo_alumnos)
        
        lista_ids_alumnos = []
        
        # recorre las alumnos	
        for dato_modelo in datos_modelo:
                # Añade las ids de los alumnos a la lista
                lista_ids_alumnos.append(dato_modelo.id_alumno)
        
        # Devuelve la lista de ids de los alumnos
        return lista_ids_alumnos

# Lee las características de un modelo de alumnos y devuelve el DataFrame
# asignando el tipo de dato adecuado a cada columna
def cambiar_tipos_columnas(df, id_modelo_alumnos, caracteristicas):
       # obtener las características del modelo de alumnos

        print("\nVoy a cambiar los tipos de columnas de id_modelo_alumnos: ", id_modelo_alumnos)

        caracteristicas_modelo_alumnos = get_list_or_404(mda_models.Caracteristica, definicion_modelo_id=id_modelo_alumnos)

        # recorre las características del modelo de alumnos
        for caracteristica in caracteristicas_modelo_alumnos:
                # Si la característica está en la lista de características
                if caracteristica.etiqueta in caracteristicas:
                        if caracteristica.tipo == mda_models.CNUMERICA:
                                # Cambia el tipo de dato de la columna a numérico
                                print ("\ncambiando tipo de dato de la columna " + caracteristica.etiqueta + " a numérico")
                                df[caracteristica.etiqueta] = pd.to_numeric(df[caracteristica.etiqueta])
                        
                        elif caracteristica.tipo == mda_models.CNO_ORDENADA:
                                # Cambia el tipo de dato de la columna a categoría no ordenada
                                print ("\ncambiando tipo de dato de la columna " + caracteristica.etiqueta + " a categoría no ordenada")
                                df[caracteristica.etiqueta] = pd.Categorical(df[caracteristica.etiqueta], ordered=False)
                        
                        elif caracteristica.tipo == mda_models.CBOOLEANA:
                                # Cambia el tipo de dato de la columna a booleano
                                print ("\ncambiando tipo de dato de la columna " + caracteristica.etiqueta + " a booleano")
                                df[caracteristica.etiqueta] = df[caracteristica.etiqueta].astype('bool')

                        # Si la característica es de tipo texto
                        elif caracteristica.tipo == mda_models.CTEXTO:
                                # Cambia el tipo de dato de la columna a texto
                                print ("\ncambiando tipo de dato de la columna " + caracteristica.etiqueta + " a texto")
                                df[caracteristica.etiqueta] = df[caracteristica.etiqueta].astype('str')
                        
                        elif caracteristica.tipo == mda_models.CORDENADA:
                                # lee los valores de la característica de valorseleccion
                                print("\ncammbiando tipo de dato de la columna " + caracteristica.etiqueta + " a categoría ordenada")
                                valores_seleccion = get_list_or_404(mda_models.ValorSeleccion, caracteristica_id=caracteristica.id) 
                                valores = []
                                # recorre los valores de la característica de valorseleccion
                                for valor_seleccion in valores_seleccion:
                                        # añade los valores a la lista
                                        valores.append(valor_seleccion.etiqueta)
                               
                                print ("\n____valores____:", valores)

                                # cambia el tipo de dato de la columna a categoría ordenada
                                df[caracteristica.etiqueta] = pd.Categorical(df[caracteristica.etiqueta], ordered=True, categories=valores)
                        

        return df        

# Generar un DataFrame leyendo los datos del modelo
# Características: lista de etiquetas de las características
# Ids alumnos: lista de ids de los alumnos
def generar_dataframe(id_modelo_alumnos, ids_alumnos, caracteristicas):

        # Crea un Data vacío
        # Las cabeceras del DataFrame son las características
        df = pd.DataFrame(columns=caracteristicas)
        
        print ("\nTIPOS DE LAS COLUMNAS antes\n",df.dtypes)
        
        # Recorre los ids de los alumnos
        for id_alumno in ids_alumnos:
                # Extrae los datos del alumno
                datos_alumno = get_list_or_404(mda_models.DatoModelo, modelo_id=id_modelo_alumnos, id_alumno=id_alumno)
                
                # Crea una lista con los datos del alumno
                lista_datos_alumno = []
                # Recorre los datos del alumno
                for dato_alumno in datos_alumno:
                        
                        # El dato del alumno está guardado como un json
                        # Convierte el json en una lista de tuplas
                        valores_alumno = json.loads(dato_alumno.datos)

                        # Por cada característica, la buscamos en valores_alumno y añadimos su valor a la lista
                        # si no está, se añade np.nan
                        for caracteristica in caracteristicas:
                                # Busca la característica en los valores del alumno
                                # Si está, añade su valor a la lista
                                # Si no está, añade np.nan
                                if caracteristica in valores_alumno:
                                        lista_datos_alumno.append(valores_alumno[caracteristica])
                                else:
                                        lista_datos_alumno.append(np.nan)

                # Añade los datos del alumno al DataFrame
                df.loc[len(df)] = lista_datos_alumno
        
        # Cambia el tipo de las columnas según se haya definido la categoría en el modelo
        df = cambiar_tipos_columnas(df, id_modelo_alumnos, caracteristicas)

        # Devuelve el DataFrame
        print ("\nTIPOS DE LAS COLUMNAS despues\n",df.dtypes)

        return df

def add_nombres_alumnos (df, ids_alumnos):
        # Añade una columna con los nombres de los alumnos
        nombres_alumnos = []
        for id_alumno in ids_alumnos:
                Alumno = get_object_or_404(cde_models.Alumno, id_alumno=id_alumno)
                nombres_alumnos.append(Alumno.nombre+" "+Alumno.apellido1+" "+Alumno.apellido2)

        df.insert(0, "Nombre", nombres_alumnos)
        return df 

def get_tm_tipo_agrupamiento(tipo_agrupamiento):

        # comparamos tipo_agrupamiento con TIPOS_AGRUPAMIENTO
        if tipo_agrupamiento == TIPOS_AGRUPAMIENTO[0][0]:
                return teammaker.TM_ALEATORIO
        elif tipo_agrupamiento == TIPOS_AGRUPAMIENTO[1][0]:
                return teammaker.TM_HOMOGENEO
        elif tipo_agrupamiento == TIPOS_AGRUPAMIENTO[2][0]:
                return teammaker.TM_HETEROGENEO
        else:
                raise TypeError("Tipo de agrupamiento no válido")

# Devuelve el tipo TeamMaker adecuado según el tipo de agrupamiento
def get_team_maker(tipo_agrupamiento, dfalumnos, verbose = False, funclog = None):
        # Dependiendo del tipo de agrupamiento, crea el obteto TeamMaker adecuado
        ta = get_tm_tipo_agrupamiento(tipo_agrupamiento)

        if ta == teammaker.TM_ALEATORIO:
                print("\n agrupando aleatoriamente")
                TM = teammaker.TMRandom(dfalumnos, verbose, funclog)
        elif ta in (teammaker.TM_HOMOGENEO,teammaker.TM_HETEROGENEO):
               print("\n agrupamiento kmeans")
               TM = teammaker.TMKmeans(dfalumnos, verbose, funclog)
        else:
                raise ValueError("Tipo de agrupamiento no válido")

        return TM 

# función de log auxiliar, solo para debug
def log(proceso = "", mensaje = ""):
    print("\n** LOG [",proceso,"] ",mensaje)            

# Realizar un agrupamiento y devuelve un objeto TeamMaker
def agrupar(alumnos_por_equipo, tipo_agrupamiento, dfalumnos, verbose = False, funclog = None):
        # Obtenemos el objeto TM adecuado al tipo de agrupamiento
        TM = get_team_maker(tipo_agrupamiento, dfalumnos, verbose, funclog)

        # Crea los equipos
        TM.crea_equipos(alumnos_por_equipo,  get_tm_tipo_agrupamiento(tipo_agrupamiento))
        
        return TM  

def guardar_equipos(TM : teammaker.TeamMaker, id_modelo, ids_alumnos):
        try:
                # Crea un objeto agrupamiento
                Agrupamiento = tc_models.Agrupamiento()
                Agrupamiento.modelo = mda_models.DefinicionModelo.objects.get(id=id_modelo)
                Agrupamiento.etiqueta = Agrupamiento.modelo.nombre
                Agrupamiento.save()

                print ("\n Agrupamiento creado: ", Agrupamiento.etiqueta)

                # recorremos los equipos generados en TM
                num_equipo = 1
                for def_equipo in TM.equiposGenerados:
                        # creamos un objeto equipo
                        Equipo = tc_models.Equipo()
                        Equipo.nombre = "Equipo " + str(num_equipo)
                        num_equipo += 1
                        Equipo.de_agrupamiento = Agrupamiento
                        Equipo.save()

                        # Añadimos el equipo al agrupamiento
                        Agrupamiento.equipos.add(Equipo)

                        print ("\n Equipo creado", Equipo.nombre)

                        # recorremos los alumnos del equipo
                        for id_alumno in def_equipo:
                                alumno_equipo = ids_alumnos[id_alumno]

                                print ("\id_alumno: ", alumno_equipo)

                                # Buscamos el alumno_equipo en la base de datos
                                Alumno = cde_models.Alumno.objects.get(id_alumno=alumno_equipo)

                                
                                print ("\nAlumno encontrado: ", Alumno)
                                Equipo.alumnos.add(Alumno)

                        # Guardamos el equipo después de añadirle los alumnos
                        Equipo.save()
                
        except Exception as e:
                raise ValueError("Error al guardar el agrupamiento: " + str(e))
        
        # guardamos el agrupamiento de nuevo
        Agrupamiento.save()

def get_id_modelo_alumnos(id_agrupamiento):
        # Busca el agrupamiento
        Agrupamiento = tc_models.Agrupamiento.objects.get(id=id_agrupamiento)
        # Busca el modelo de alumnos
        ModeloAlumnos = Agrupamiento.modelo
        # Devuelve el id del modelo de alumnos
        return ModeloAlumnos.id
        
# Devuelve una lista con los ids de los alumnos de un equipo       
def get_ids_alumnos_equipo(id_agrupamiento, id_equipo):
        # Busca el equipo
        Equipo = tc_models.Equipo.objects.get(de_agrupamiento_id=id_agrupamiento, id=id_equipo)

        Alumnos = Equipo.alumnos.all()
        # Recorre los alumnos del equipo
        ids_alumnos = []
        for Alumno in Alumnos:
                ids_alumnos.append(Alumno.id_alumno)
        
        return ids_alumnos
                       
# Devuelve el nombre de un equipo
def get_nombre_equipo(id_agrupamiento, id_equipo):
        # Busca el equipo
        Equipo = tc_models.Equipo.objects.get(de_agrupamiento_id=id_agrupamiento, id=id_equipo)
        # Devuelve el nombre del equipo
        return Equipo.nombre