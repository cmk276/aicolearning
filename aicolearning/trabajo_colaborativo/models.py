from django.db import models
from modelos_de_alumnos.models import DefinicionModelo
from centro_de_estudios.models import Alumno

class Equipo(models.Model):
    nombre = models.CharField("nombre", max_length=100, null=True)
    alumnos = models.ManyToManyField(Alumno)

# Create your models here.
class Agrupamiento(models.Model):
    etiqueta = models.CharField("etiqueta", max_length=200, null=True)
    modelo = models.ForeignKey(DefinicionModelo, on_delete=models.CASCADE, null=True)
    equipos = models.ForeignKey("Equipo", on_delete=models.CASCADE, null=True) 

    def __str__(self):
        return self.etiqueta
    

