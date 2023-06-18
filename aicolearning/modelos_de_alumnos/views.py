from django.shortcuts import get_object_or_404,  get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.db import models
from .forms import FormImportarModelo
from .models import DefinicionModelo, Caracteristica, DatoModelo
import pandas as pd
from django.views.generic import ListView


# Importamos los modelos del centro de estudios
from centro_de_estudios import models 

class VistaModelos(generic.ListView):
    template_name = "modelos_de_alumnos/modelos.html"
    paginate_by = 10  # Cantidad de registros por página
    queryset = DefinicionModelo.objects.order_by("nombre")
    context_object_name = "lista_modelos"



class DetailView(generic.DetailView):
    model = DefinicionModelo
    template_name = "modelos_de_alumnos/detail.html"


# útiles para el formulario ImportarModelo
#Leer un fichero csv y convertirlo a un pandas dataframe
def leer_csv(fichero):
    df = pd.read_csv(fichero, sep=';', encoding='utf-8')
    return df

# guardar las filas del dataframe en la tabla DatoModelo
#Crear un modelo de alumnos a partir de un dataframe

def crear_modelo_alumnos(df, nombre_modelo):
    modelo = DefinicionModelo(nombre=nombre_modelo)
    modelo.save()

    # extraemos las cuatro primeras columnas del dataframe
    datos_alumnos = df.columns[0:4]

    # Quitamos de df las cuatro primeras columnas que corresponden a los datos de identificación de los alumnos
    df = df.drop(df.columns[0:4], axis=1)
    # Recorremos el resto del dataset y creamos las características
    for columna in df.columns:
        caracteristica = Caracteristica(etiqueta=columna, definicion_modelo=modelo)
        caracteristica.save()
    return modelo.id


def guardar_filas(df, id_modelo):
    # recorremos las filas del dataframe
    for index, row in df.iterrows():
        # la primera columna del dataframe es el id del alumno
        id_alumno = row[0]
        nombre_alumno = row[1]
        apellido_1 = row[2]
        apellido_2 = row[3]

        # si el alumno no existe en la tabla Alumno lo creamos
        if not models.Alumno.objects.filter(id_alumno=id_alumno).exists():
            alumno = models.Alumno(id_alumno=id_alumno, nombre=nombre_alumno, apellido1=apellido_1, apellido2=apellido_2)
            alumno.save()
            print ("\n Creando alumno id_alumno: "+str(id_alumno))

        # Cargamos el modelo id_modelo
        modelo = DefinicionModelo.objects.get(id=id_modelo)

        # Guardamos de la cuarta columna en adelante que son los datos del alumno como un json
        datos_modelo = row[4:].to_json()


        # Creamos un objeto DatoModelo con los datos del alumno
        dato_modelo = DatoModelo(id_alumno=id_alumno, datos=datos_modelo, modelo=modelo)
        dato_modelo.save()
        print ("\n *** Guardando datos del alumno id_alumno: "+str(id_alumno))


#Crear un modelo de alumnos a partir de un dataframe
def crear_modelo_alumnos(df, nombre_modelo):
    modelo = DefinicionModelo(nombre=nombre_modelo)
    modelo.save()

    # extraemos las cuatro primeras columnas del dataframe
    datos_alumnos = df.columns[0:4]

    # Quitamos de df las cuatro primeras columnas que corresponden a los datos de identificación de los alumnos
    df = df.drop(df.columns[0:4], axis=1)
    # Recorremos el resto del dataset y creamos las características
    for columna in df.columns:
        caracteristica = Caracteristica(etiqueta=columna, definicion_modelo=modelo)
        caracteristica.save()
    return modelo.id

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

class VistaModelo(ListView):
    model = DatoModelo
    template_name = "modelos_de_alumnos/modelo.html"
    context_object_name = "datos_modelo"

    def get_queryset(self):
        # Recupera los datos de un solo modelo
        return DatoModelo.objects.filter(modelo_id=self.kwargs['id_modelo'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recupera el modelo
        modelo = DefinicionModelo.objects.get(id=self.kwargs['id_modelo'])

        print ("\n *** Recuperando modelo: "+str(modelo.nombre))

        context['modelo'] = modelo
        for dato in context['datos_modelo']:
            print ("\n *** Recuperando alumno: "+str(dato.id_alumno))
            dato.alumno = models.Alumno.objects.get(id_alumno=dato.id_alumno)
            
            print ("\n *** Recuperando datos del alumno: "+str(dato.lista_datos()))

        
        return context