from django.contrib import admin

# Register your models here.
from .models import CentroDeEstudios, Profesor, Alumno, Estudio, Curso, Asignatura, Grupo
admin.site.register(CentroDeEstudios)
admin.site.register(Profesor)
admin.site.register(Alumno)
admin.site.register(Estudio)
admin.site.register(Curso)
admin.site.register(Asignatura)
admin.site.register(Grupo)

