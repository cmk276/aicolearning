from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .forms import FormConfigurarAgrupamiento 
from django.views import generic
from django.db import models
from django.views import View
from django.views.generic.edit import FormView
# importar trabajo_colaborativo_utiles
from . import trabajo_colaborativo_utiles as tcu


# Importamos los modelos del modelo de alumnos
from modelos_de_alumnos import models

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return HttpResponse("Hello, world. You're at the trabajo colaborativo index.")

# clase de vista que muestra el formulario de configuración de agrupamiento
# recibe como parámetro el id del modelo de alumnos para el que se va a configurar el agrupamiento
class VistaConfigurarAgrupamiento(View):
    caracteristicas = []
    cadena_ids_alumnos = ""

    # Inicialización de la vista
    def setup(self, request, *args, **kwargs):

        # llama al método setup de la clase padre
        super().setup(request, *args, **kwargs)

        id_modelo_alumnos = kwargs["id_modelo_alumnos"]
        # Obtenemos las características del modelo de alumnos
        self.caracteristicas = tcu.get_caracteristicas_modelo_alumnos(id_modelo_alumnos)

        # Guardamos la cadena de ids de alumnos para la confirmación del agrupamiento (siguiente formulario)
        self.cadena_ids_alumnos = kwargs["ids_alumnos"]
        
    def get(self, request, id_modelo_alumnos, num_alumnos, num_alumnos_por_grupo, ids_alumnos):
        
        # crea el formulario de configuración de agrupamiento
        form = FormConfigurarAgrupamiento()
        
        # añade las características al formulario
        form.fields["alumnos_por_grupo"].initial = num_alumnos_por_grupo
        form.fields["caracteristicas"].choices = [(caracteristica, caracteristica) for caracteristica in self.caracteristicas]
        context = {'form': form}
        return render(request, 
                      "trabajo_colaborativo/configurar_agrupamiento.html", 
                      context)

    def post(self, request, id_modelo_alumnos, num_alumnos, num_alumnos_por_grupo, ids_alumnos):
        print("\nV ***POST ---- id_modelo_alumnos: ", id_modelo_alumnos)

        #self.caracteristicas = tcu.get_caracteristicas_modelo_alumnos(id_modelo_alumnos)

        print("\nV ***POST ---- Caracteristicas: ", self.caracteristicas)
        form = FormConfigurarAgrupamiento(request.POST)
        # añade las características al formulario
        form.fields["alumnos_por_grupo"].initial = num_alumnos_por_grupo
        form.fields["caracteristicas"].choices = [(caracteristica, caracteristica) for caracteristica in self.caracteristicas]

        if form.is_valid():
            tipo_agrupamiento = form.cleaned_data['tipo_agrupamiento']
            caracteristicas = form.cleaned_data['caracteristicas']
            num_alumnos_por_grupo = form.cleaned_data['alumnos_por_grupo']

            print("V \n FORMULARIO RECIBIDO: Tipo agrupamiento[" + str(tipo_agrupamiento) + "]\n"+str(caracteristicas))
            
            # imprimimos los ids de los alumnos
            print("V \n IDS ALUMNOS: " + self.cadena_ids_alumnos)

            # Obtenemos los ids de las características seleccionadas en el form
            ids_caracteristicas = tcu.get_ids_caracteristicas(id_modelo_alumnos, caracteristicas)
            # Generamos la cadena para pasarla como parámetro
            cadena_ids_caracteristicas = ','.join(str(id_caracteristica) for id_caracteristica in ids_caracteristicas)

            print("V \n IDS CARACTERISTICAS: " + cadena_ids_caracteristicas)

            # Generamos la URL para la vista agrupar
            url = reverse('trabajo_colaborativo:agrupar', kwargs={'id_modelo_alumnos': id_modelo_alumnos,
                                                                    'alumnos_por_grupo': num_alumnos_por_grupo,
                                                                    'tipo_agrupamiento': tipo_agrupamiento,
                                                                    'ids_caracteristicas': cadena_ids_caracteristicas,
                                                                    'ids_alumnos': self.cadena_ids_alumnos
                                                                    })
            
            print ("V \n URL: " + url)
            
            # redirigimos a la vista agrupar
            return HttpResponseRedirect(url)
        else:
            num_alumnos_por_grupo = form.cleaned_data['alumnos_por_grupo']
            print("V \n FORMULARIO NO VÁLIDO:" + str(form.errors))

            # volvemos a la página de configuración de agrupamiento con los datos recibidos para que se solucionen los errores
            url = reverse('trabajo_colaborativo:configurar_agrupamiento', kwargs={'id_modelo_alumnos': id_modelo_alumnos, 
                                                                                  'num_alumnos': num_alumnos, 
                                                                                  'num_alumnos_por_grupo': num_alumnos_por_grupo, 
                                                                                  'ids_alumnos': self.cadena_ids_alumnos})
            return HttpResponseRedirect(url)

# Vista temporal mientras se lanza el agrupador
class VistaTempAgrupando(View):
    def get(self, request, id_modelo_alumnos, alumnos_por_grupo, tipo_agrupamiento, ids_alumnos):
        return render(request, 'trabajo_colaborativo/temp_agrupando.html')

# Vista que realiza el agrupamiento y envía a la pantalla de confirmación del agrupamiento realizado
class VistaAgrupar(View):

    # Datos que va a necesitar el agrupador
    ids_caracteristicas = []
    ids_alumnos = []

    # Inicialización de la vista
    def setup(self, request, *args, **kwargs):

        # llama al método setup de la clase padre
        super().setup(request, *args, **kwargs)

        print("\nVistaAgrupar ***setup ---- kwargs: ", kwargs)

        # Obtenemos los datos necesarios
        id_modelo_alumnos = kwargs["id_modelo_alumnos"]

        # Alumnos por grupo
        self.num_alumnos_por_grupo = kwargs["alumnos_por_grupo"]

        # Tipo de agrupamiento
        self.tipo_agrupamiento = kwargs["tipo_agrupamiento"]

        # Obtenemos los ids de los alumnos
        cadena_ids_alumnos = kwargs["ids_alumnos"]
        if (cadena_ids_alumnos == ""):
            # No se pasan alumnos como parámetro, se obtienen todos los alumnos asociados al modelo
            self.ids_alumnos = tcu.get_ids_alumnos_modelo(id_modelo_alumnos)
        else:
            # Se pasan alumnos como parámetro
            # cadena_ids_alumnos es una lista separada por comas de los ids de los alumnos
            # convertirlo a lista
            self.ids_alumnos = cadena_ids_alumnos.split(",")

        # Obtenemos los ids de las características del modelo de alumnos
        cadena_ids_caracteristicas = kwargs["ids_caracteristicas"]
        if (cadena_ids_caracteristicas == ""):
            # No se pasan características como parámetro, se obtienen todas las características asociadas al modelo
            self.ids_caracteristicas = tcu.get_ids_caracteristicas_modelo_alumnos(id_modelo_alumnos)
        else:
            # Se pasan características como parámetro
            # cadena_ids_caracteristicas es una lista separada por comas de los ids de las características
            # convertirlo a lista
            self.ids_caracteristicas = cadena_ids_caracteristicas.split(",")
        
        print ("\nVistaAgrupar ***setup ---- ids_alumnos: ", self.ids_alumnos)
        print ("\nVistaAgrupar ***setup ---- caracteristicas: ", self.ids_caracteristicas)
        
    def get(self, requesr, *args, **kwargs):

        # REALIZAR AGRUPAMIENTO    

        return render(request, 'trabajo_colaborativo/temp_agrupando.html')
                                                                              







"""
class FormViewConfigurarAgrupamiento(FormView):
    template_name = "trabajo_colaborativo/configurar_agrupamiento.html"
    form_class = FormConfigurarAgrupamiento
    success_url = 'confirmar_agrupamiento'
    caracteristicas = []

    def get_context_data(self, **kwargs):
        context = super(FormViewConfigurarAgrupamiento, self).get_context_data(**kwargs)

        context['id_modelo_alumnos'] = self.kwargs['id_modelo_alumnos']
        context['num_alumnos'] = self.kwargs['num_alumnos']
        # La lista de características se ha creado en el método get()
        context['caracteristicas'] = [(caracteristica, caracteristica) for caracteristica in self.caracteristicas]

        print ("\nV ***GET_CONTEXT_DATA ---- CARACTERÍSTICAS: ", context['caracteristicas'])
        return context
    
    def get_form(self, form_class=None):

        form = super().get_form(form_class)
        
        # Modificar el contenido del campo características
        form.fields["caracteristicas"].choices = [(caracteristica, caracteristica) for caracteristica in self.caracteristicas]

        return form

    # get
    def get(self, request, *args, **kwargs):

        print("\n V Método get()")

        print(kwargs["id_modelo_alumnos"])
        # extrae las lista de características del modelo de alumnos
        id_modelo_alumnos = kwargs["id_modelo_alumnos"]
        self.caracteristicas = tcu.get_caracteristicas_modelo_alumnos(id_modelo_alumnos)
        
        inicial = super(FormViewConfigurarAgrupamiento, self).get(request, *args, **kwargs)

        
        print("\nV Método get()  ---- CARACTERÍSTICAS: ", self.caracteristicas)


        return inicial 
    
    # post
    def post(self, request, *args, **kwargs):
        print ("\nV Método post()")
        id_modelo_alumnos = kwargs["id_modelo_alumnos"]
        self.caracteristicas = tcu.get_caracteristicas_modelo_alumnos(id_modelo_alumnos)

        print("\nV Método post()  ---- CARACTERÍSTICAS: ")
        print(kwargs)

        return super(FormViewConfigurarAgrupamiento, self).post(request, *args, **kwargs)
"""