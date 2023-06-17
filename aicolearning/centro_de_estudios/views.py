from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.db import models
from .models import Alumno
from django.views import generic
from django.core.paginator import Paginator, EmptyPage

# Clase para gestionar el listado de agrupamientos
class VistaAlumnos(ListView):
    paginate_by = 10  # Cantidad de registros por página
    queryset = Alumno.objects.order_by("apellido1","apellido2","nombre")
    template_name = 'centro_de_estudios/alumnos.html'
    context_object_name = 'alumnos'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Titulo de la página	
        context['titulo'] = "Alumnos"

        return context



