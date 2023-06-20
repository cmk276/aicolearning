'''
AICoLearning
Herramienta web para la creación de grupos colaborativos asistida por Machine Learning
Código desarrollado por: Francisco Tejeira Bújez
Para el Proyecto fin de Grado de Ingeniería Informática de la UNIR
2023
'''
from django.db import models
from modelos_de_alumnos.models import DefinicionModelo, Caracteristica
from centro_de_estudios.models import Alumno

class Equipo(models.Model):
    nombre = models.CharField("nombre", max_length=100, null=True)
    alumnos = models.ManyToManyField(Alumno)
    de_agrupamiento = models.ForeignKey("Agrupamiento", on_delete=models.CASCADE, null=True)

# Create your models here.
class Agrupamiento(models.Model):
    
    etiqueta = models.CharField("etiqueta", max_length=200, null=True)
    modelo = models.ForeignKey(DefinicionModelo, on_delete=models.CASCADE, null=True)
    equipos = models.ManyToManyField(Equipo)
    tipo = models.CharField("tipo", max_length=20, null=True)
    caracteristicas = models.ManyToManyField(Caracteristica, blank=True)

    def __str__(self):
        return self.etiqueta
    

