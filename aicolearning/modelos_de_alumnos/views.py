from django.shortcuts import get_object_or_404,  get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic

from aicolearning.modelos_de_alumnos.modelos_de_alumnos_utiles import crear_modelo_alumnos, guardar_filas, leer_csv
from .forms import FormImportarModelo
from .models import DefinicionModelo

# FICHERO CON INFO CORRECTA

# Importamos los modelos del centro de estudios

class IndexView(generic.ListView):
    template_name = "modelos_de_alumnos/index.html"
    context_object_name = "modelo_list"

    def get_queryset(self):
        """Devuelve los modelos ordenados por nombre"""
        return DefinicionModelo.objects.order_by("id")


class DetailView(generic.DetailView):
    model = DefinicionModelo
    template_name = "modelos_de_alumnos/detail.html"


# útiles para el formulario ImportarModelo
#Leer un fichero csv y convertirlo a un pandas dataframe
# guardar las filas del dataframe en la tabla DatoModelo
#Crear un modelo de alumnos a partir de un dataframe
# Vista para importar un modelo de alumnos a partir del formulario FormImportarModelo
def importar(request):
    if request.method == 'POST':
        form = FormImportarModelo(request.POST, request.FILES)
        if form.is_valid():
            nombre_modelo = form.cleaned_data['nombre_modelo']
            fichero_csv = form.cleaned_data['fichero_csv']
            
            # leer el fichero csv y convertirlo a un pandas dataframe
            df = leer_csv(fichero_csv)
            
            # crrear un modelo de alumnos a partir del dataframe
            modelo = crear_modelo_alumnos(df, nombre_modelo)

            # guardar las filas del dataframe en la tabla DatoModelo
            guardar_filas(df, modelo)
            
            # va la vista de modelos de alumnos
            return HttpResponseRedirect(reverse('modelos_de_alumnos:modelo',args=[modelo]))
    else:
        form = FormImportarModelo()
    
    return render(request, 'modelos_de_alumnos/importar_modelo.html', {'form': form})