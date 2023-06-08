import pandas as pd
#from ........users.fteje.documents.code.aicolearning.aicolearning.centro_de_estudios import models
from ..centro_de_estudios import models
from django.db import models
from aicolearning.modelos_de_alumnos.models import Caracteristica, DatoModelo, DefinicionModelo


def crear_modelo_alumnos(df, nombre_modelo):
    modelo = DefinicionModelo(nombre=nombre_modelo)
    modelo.save()

    # extraemos las cuatro primeras columnas del dataframe
    datos_alumnos = df.columns[0:4]

    # Quitamos de df las cuatro primeras columnas que corresponden a los datos de identificación de los alumnos
    df = df.drop(df.columns[0:4], axis=1)
    # Recorremos el resto del dataset y creamos las características
    for columna in df.columns:
        caracteristica = Caracteristica(etiqueta=columna, definicion_modelo=modelo)
        caracteristica.save()
    return modelo.id


def guardar_filas(df, id_modelo):
    # recorremos las filas del dataframe
    for index, row in df.iterrows():
        # la primera columna del dataframe es el id del alumno
        id_alumno = row[0]
        nombre_alumno = row[1]
        apellido_1 = row[2]
        apellido_2 = row[3]

        # si el alumno no existe en la tabla Alumno lo creamos
        if not models.Alumno.objects.filter(id_alumno=id_alumno).exists():
            alumno = models.Alumno(id_alumno=id_alumno, nombre=nombre_alumno, apellido1=apellido_1, apellido2=apellido_2)
            alumno.save()
            print ("\n Creando alumno id_alumno: "+str(id_alumno))

        # Cargamos el modelo id_modelo
        modelo = DefinicionModelo.objects.get(id=id_modelo)

        # Guardamos de la cuarta columna en adelante que son los datos del alumno como un json
        datos_modelo = row[4:].to_json()


        # Creamos un objeto DatoModelo con los datos del alumno
        dato_modelo = DatoModelo(id_alumno=id_alumno, datos=datos_modelo, modelo=modelo)
        dato_modelo.save()
        print ("\n *** Guardando datos del alumno id_alumno: "+str(id_alumno))


def leer_csv(fichero):
    df = pd.read_csv(fichero, sep=';', encoding='utf-8')
    return df