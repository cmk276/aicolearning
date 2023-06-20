'''
AICoLearning
Herramienta web para la creación de grupos colaborativos asistida por Machine Learning
Código desarrollado por: Francisco Tejeira Bújez
Para el Proyecto fin de Grado de Ingeniería Informática de la UNIR
2023
'''
from django.urls import path

from . import views

urlpatterns = [
    path("", views.VistaAlumnos.as_view(), name="alumnos"),
]