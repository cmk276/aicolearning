from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from .forms import FormConfigurarAgrupamiento 
from django.views import generic 
from django.views.generic import ListView
from django.db import models
from trabajo_colaborativo.models import Agrupamiento
from django.views import View
from django.views.generic.edit import FormView
import pandas as pd
# importar trabajo_colaborativo_utiles
from . import trabajo_colaborativo_utiles as tcu
from . import teammaker as teammaker


# Importamos los modelos del modelo de alumnos
from modelos_de_alumnos import models

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    #return HttpResponse("Hello, world. You're at the trabajo colaborativo index.")
    return render(request,"trabajo_colaborativo/index.html")

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
    caracteristicas = []
    ids_alumnos = []

    # Inicialización de la vista
    def setup(self, request, *args, **kwargs):

        # llama al método setup de la clase padre
        super().setup(request, *args, **kwargs)

        print("\nVistaAgrupar ***setup ---- kwargs: ", kwargs)

        # Obtenemos los datos necesarios
        self.id_modelo_alumnos = kwargs["id_modelo_alumnos"]

        # Alumnos por grupo
        self.num_alumnos_por_grupo = kwargs["alumnos_por_grupo"]

        # Tipo de agrupamiento
        self.tipo_agrupamiento = kwargs["tipo_agrupamiento"]

        # Obtenemos los ids de los alumnos
        cadena_ids_alumnos = kwargs["ids_alumnos"]
        if (cadena_ids_alumnos == ""):
            # No se pasan alumnos como parámetro, se obtienen todos los alumnos asociados al modelo
            self.ids_alumnos = tcu.get_ids_alumnos_modelo(self.id_modelo_alumnos)
        else:
            # Se pasan alumnos como parámetro
            # cadena_ids_alumnos es una lista separada por comas de los ids de los alumnos
            # convertirlo a lista
            self.ids_alumnos = cadena_ids_alumnos.split(",")

        # Obtenemos los ids de las características del modelo de alumnos
        cadena_ids_caracteristicas = kwargs["ids_caracteristicas"]
        if (cadena_ids_caracteristicas == ""):
            # No se pasan características como parámetro, se obtienen todas las características asociadas al modelo
            self.ids_caracteristicas = tcu.get_ids_caracteristicas_modelo_alumnos(self.id_modelo_alumnos)
        else:
            # Se pasan características como parámetro
            # cadena_ids_caracteristicas es una lista separada por comas de los ids de las características
            # convertirlo a lista
            self.ids_caracteristicas = cadena_ids_caracteristicas.split(",")
        
        # Obtenemos las etiquetas de las características
        self.caracteristicas = tcu.get_etiquetas_caracteristicas(self.id_modelo_alumnos, self.ids_caracteristicas)

        print ("\nVistaAgrupar ***setup ---- ids_alumnos: ", self.ids_alumnos)
        print ("\nVistaAgrupar ***setup ---- ids_caracteristicas: ", self.ids_caracteristicas)
        
    def get(self, request, *args, **kwargs):

        # Se prepara un dataframe con los datos de los alumnos y las características
        print("\n PREPARANDO Dataframe")
        df = tcu.generar_dataframe(self.id_modelo_alumnos,self.ids_alumnos, self.caracteristicas)
        print("\n DataFrame: \n", df)
        
        # REALIZAR AGRUPAMIENTO    
        TM = tcu.agrupar(self.num_alumnos_por_grupo, self.tipo_agrupamiento, df, True, tcu.log)
        
        # Guardamos el agrupamiento en la base de datos
        print ("\nEQUIPOS CREADOS: \n", TM.equiposGenerados)

        id_agrupamiento = tcu.guardar_equipos(TM, self.id_modelo_alumnos ,self.ids_alumnos)
                                                                              
        # Generamos la URL para ver el listado de los equipos generados en el agrupamiento
        url = reverse('trabajo_colaborativo:ver_equipos', kwargs={'id_agrupamiento' : id_agrupamiento, 'mostrar_info': 1})

        return HttpResponseRedirect(url)
        

class VistaEquipo(View):

    def get(self, request, id_agrupamiento, id_equipo, mostrar_info, ids_caracteristicas):
        
        caracteristicas = []

        # buscamos el modelo al que pertenece el agrupamiento
        id_modelo_alumnos = tcu.get_id_modelo_alumnos(id_agrupamiento)

        # Si mostrar_info es 1, se cargan los literales de las características
        if (mostrar_info == 1):

            if (ids_caracteristicas==""):
                
                # Mostrar info y sin ids_características: se muestran todas las características
                caracteristicas = tcu.get_caracteristicas_modelo_alumnos(id_modelo_alumnos)
            else:
                # Se muestran solo las etiquetas de las características pasadas como parámetro
                ids_caracteristicas = ids_caracteristicas.split(",")
                caracteristicas = tcu.get_etiquetas_caracteristicas(id_modelo_alumnos, ids_caracteristicas)
        else:
            caracteristicas = []

        # Obtenemos los ids de los alumnos del equipo
        ids_alumnos = tcu.get_ids_alumnos_equipo(id_agrupamiento, id_equipo)
        
        # Si se van a usar características, se genera el dataframe
        if (len(caracteristicas) > 0):
            # Obtenemos el dataframe del equipo insertando los nombres de los alumnos en la primera columna
            df_equipo = tcu.generar_dataframe(id_modelo_alumnos, ids_alumnos, caracteristicas)
        else:
            df_equipo = pd.DataFrame()
        
        df_equipo = tcu.add_nombres_alumnos(df_equipo, ids_alumnos)

        tabla_html = df_equipo.to_html(index=False)
        
        nombre_equipo = tcu.get_nombre_equipo(id_agrupamiento, id_equipo)
        return render(request, 'trabajo_colaborativo/vista_equipo.html', {'tabla_html': tabla_html, 'nombre_equipo': nombre_equipo})

# Esta vista sí accede directamente a los modelos de la base de datos
class VistaEquipos (View):
    def get(self, request, id_agrupamiento, mostrar_info, ids_caracteristicas):

        print("------------------ VistaEquipos ------------------")
        site_url = "http://" + request.META['HTTP_HOST']

        # Buscamos el nombre del agrupamiento
        agrupamiento = get_object_or_404(Agrupamiento,id=id_agrupamiento)
        print ("\nNombre agrupamiento: ", agrupamiento.etiqueta)
        print ("\n ids_caracteristicas: ", ids_caracteristicas)

        # Vamos a enviar una lista de diccionarios con los datos de los equipos
        datos = []

        # por cada equipo del agrupamiento, generamos el enlace a la vista de equipo
        for equipo in agrupamiento.equipo_set.all():
            print ("\nEquipo: ", equipo.nombre)
            # Obtenemos el número de alumnos de ese equipo
            num_alumnos = equipo.alumnos.count()

            print("\n num_alumnos: ", num_alumnos)

            if ids_caracteristicas == "":
                url = reverse('trabajo_colaborativo:ver_equipo', args=[id_agrupamiento, equipo.id, mostrar_info])
            else:
                url = reverse('trabajo_colaborativo:ver_equipo', args=[id_agrupamiento, equipo.id, mostrar_info, ids_caracteristicas])

            print ("\nURL: ", url)
            datos.append({'nombre_equipo': equipo.nombre, 'num_alumnos': num_alumnos, 'url': site_url+url})

        # renderizamos la vista del listado de equipos
        print (datos)
        return render(request, 'trabajo_colaborativo/ver_equipos.html', {'equipos': datos, 'titulo': agrupamiento.etiqueta})

# Clase para gestionar el listado de agrupamientos
class VistaAgrupamientos(ListView):
    #model = Agrupamiento
    queryset = Agrupamiento.objects.order_by("etiqueta")
    template_name = 'trabajo_colaborativo/agrupamientos.html'
    paginate_by = 10
    context_object_name = 'agrupamientos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Titulo de la página	
        context['titulo'] = "Agrupamientos"

        # Recorremos los agrupamientos para añadir datos adicionales
        for agrupamiento in context['agrupamientos']:
            # Obtenemos el modelo de alumnos al que pertenece el agrupamiento y lo añadimos al contexto
            modelo_alumnos = agrupamiento.modelo

            # Obtenemos los datos del modelo de alumnos
            num_alumnos = models.DatoModelo.objects.filter(modelo=modelo_alumnos).count()
            
            # Calculamos los equipos que se han generado en el agrupamiento
            num_equipos = agrupamiento.equipos.count()

            # Generamos la URL para ver el listado de los equipos generados en el agrupamiento
            site_url = "http://" + self.request.META['HTTP_HOST']
            url_agrupamiento = site_url+reverse('trabajo_colaborativo:ver_equipos', args=[agrupamiento.id, 1])


            # Añadimos los datos al contexto
            agrupamiento.num_alumnos = num_alumnos
            agrupamiento.num_equipos = num_equipos
            agrupamiento.url_agrupamiento = url_agrupamiento

        
        print ("\nContexto: ", context)
        return context
