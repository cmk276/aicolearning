'''
AICoLearning
Herramienta web para la creación de grupos colaborativos asistida por Machine Learning
Código desarrollado por: Francisco Tejeira Bújez
Para el Proyecto fin de Grado de Ingeniería Informática de la UNIR
2023
'''
import json
from django.db import models

CNUMERICA = "NU"
CNO_ORDENADA = "NO"
CTEXTO = "TE"
CBOOLEANA = "BO"
CORDENADA = "OR"

# Create your models here.
class DefinicionModelo(models.Model):
    nombre = models.CharField("nombre", max_length=50)
    descripcion = models.TextField("descripcion", blank=True, null=True)
    caracteristicas = models.ManyToManyField("Caracteristica")

    def cadena_caracteristicas(self):
        # recorremos las características y devolvemos una cadena con el nombre de las 10 primeras
        cadena = ""
        # obtenemos las características del modelo con id
        caracteristicas = Caracteristica.objects.filter(definicion_modelo=self.id)[:5]
        for caracteristica in caracteristicas:
            cadena = cadena + caracteristica.etiqueta + ", "
        return cadena    

    def __str__(self):
        return self.nombre
    
class Caracteristica(models.Model):
    
    ELECCION_TIPOS_CARACTERISTICAS = [
        (CNUMERICA, "Numérica"),
        (CNO_ORDENADA, "No Ordenada"),
        (CTEXTO, "Texto"),
        (CBOOLEANA, "Verdadero/Falso"),
        (CORDENADA, "Ordenada")
    ]
    etiqueta = models.CharField("etiqueta", max_length=100)
    descripcion = models.TextField
    definicion_modelo = models.ForeignKey(DefinicionModelo, on_delete=models.CASCADE)
    
    # Campo Tipo es una selección de distintos valores
    tipo = models.CharField(
        max_length=2,
        choices=ELECCION_TIPOS_CARACTERISTICAS,
        default=CNUMERICA,
    )

    def __str__(self):
        return self.etiqueta
    
class ValorSeleccion(models.Model):
    num_orden = models.IntegerField("número de orden")
    etiqueta = models.CharField("nombre", max_length=100) 
    caracteristica = models.ForeignKey(Caracteristica, on_delete=models.CASCADE)

    def __str__(self):
        return self.etiqueta
    
class DatoModelo(models.Model):
    id_alumno = models.CharField("id_alumno", max_length=10) 
    modelo = models.ForeignKey(DefinicionModelo, on_delete=models.CASCADE)
    datos = models.JSONField("datos")

    def cadena_datos(self):
        datos= json.loads(self.datos)
        
        # Extraemos una lista con los valores del diccionario datos
        lista_datos = list(datos.values())

        # recorremos lista_datos para ir añadiendo los cinco primeros valores a una cadena
        cadena = ""
        for i in range(0,5):
            try:
                cadena = cadena + str(lista_datos[i]) + ",  "
            except:
                # salimos del bucle cuando no quedan más valores en lista_datos
                break
        
        return cadena

    def __str__(self):
        return str(self.modelo.id)+" "+self.id_alumno