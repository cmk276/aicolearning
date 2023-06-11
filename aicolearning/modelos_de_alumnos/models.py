from django.db import models

CNUMERICA = "NU"
CNO_ORDENADA = "NO"
CTEXTO = "TE"
CBOOLEANA = "BO"
CORDENADA = "OR"

# Create your models here.
class DefinicionModelo(models.Model):
    nombre = models.CharField("nombre", max_length=50)
    descripcion = models.TextField
    caracteristicas = models.ManyToManyField("Caracteristica")

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
    def __str__(self):
        return str(self.modelo.id)+" "+self.id_alumno