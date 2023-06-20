'''
AICoLearning
Herramienta web para la creación de grupos colaborativos asistida por Machine Learning
Código desarrollado por: Francisco Tejeira Bújez
Para el Proyecto fin de Grado de Ingeniería Informática de la UNIR
2023
'''
from django.apps import AppConfig


class ModelosDeAlumnosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modelos_de_alumnos"
