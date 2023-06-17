from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.db import models
from .models import Alumno
from django.views import generic

# Clase para gestionar el listado de agrupamientos
class VistaAlumnos(ListView):
    model = Alumno
    template_name = 'centro_de_estudios/alumnos.html'
    context_object_name = 'alumnos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Titulo de la página	
        context['titulo'] = "Alumnos"

        # Lista de alumnos
        context['alumnos'] = Alumno.objects.all().order_by('apellido1', 'apellido2', 'nombre')
        return context



