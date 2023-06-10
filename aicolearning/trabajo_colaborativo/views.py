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
    #template = "trabajo_colaborativo/configurar_agrupamiento.html"
    caracteristicas = []

    def get(self, request, id_modelo_alumnos, num_alumnos, num_alumnos_por_grupo):
        
        print("\nV ***GET ---- id_modelo_alumnos: ", id_modelo_alumnos)

        self.caracteristicas = tcu.get_caracteristicas_modelo_alumnos(id_modelo_alumnos)

        print("V caracteristicas: ", self.caracteristicas)
        
        # crea el formulario de configuración de agrupamiento
        form = FormConfigurarAgrupamiento()
        # añade las características al formulario
        form.fields["alumnos_por_grupo"].initial = num_alumnos_por_grupo
        form.fields["caracteristicas"].choices = [(caracteristica, caracteristica) for caracteristica in self.caracteristicas]

        context = {'form': form}
        return render(request, 
                      "trabajo_colaborativo/configurar_agrupamiento.html", 
                      context)

    def post(self, request, id_modelo_alumnos, num_alumnos, num_alumnos_por_grupo):
        print("\nV ***POST ---- id_modelo_alumnos: ", id_modelo_alumnos)

        self.caracteristicas = tcu.get_caracteristicas_modelo_alumnos(id_modelo_alumnos)

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
            return HttpResponseRedirect(reverse_lazy('trabajo_colaborativo:index'))
        
            
        else:
            num_alumnos_por_grupo = form.cleaned_data['alumnos_por_grupo']
            print("V \n FORMULARIO NO VÁLIDO:" + str(form.errors))

            # volvemos a la página de configuración de agrupamiento con los datos recibidos
            url = reverse('trabajo_colaborativo:configurar_agrupamiento', kwargs={'id_modelo_alumnos': id_modelo_alumnos, 'num_alumnos': num_alumnos, 'num_alumnos_por_grupo': num_alumnos_por_grupo})
            print("\nV ***POST ---- URL NO VALIDO: ", url)
            return HttpResponseRedirect(url)
            


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
