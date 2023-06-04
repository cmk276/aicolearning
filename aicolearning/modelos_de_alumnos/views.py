from django.shortcuts import get_object_or_404,  get_list_or_404, render
from django.http import HttpResponse
from .models import DefinicionModelo, Caracteristica
from django.template import loader
from django.http import Http404


def index(request):
    DefinicionesDeModelos = DefinicionModelo.objects.order_by("nombre")
    template = loader.get_template("modelos_de_alumnos/index.html")
    context = {
        "modelo_list": DefinicionesDeModelos,
    }
    
    return HttpResponse(template.render(context, request))

def importar(request, modelo_id):
    return render(request, "modelos_de_alumnos/importar.html", {"modelo_id" : modelo_id})

def modelo(request, modelo_id):

    Modelo = get_object_or_404(DefinicionModelo, pk=modelo_id) 
    #Caracteristicas =  get_list_or_404(Caracteristica,definicion_modelo=modelo_id)
    
    Caracteristicas = Caracteristica.objects.filter(definicion_modelo=modelo_id)
    return render(request, "modelos_de_alumnos/detail.html", {"modelo": Modelo, "caracteristicas": Caracteristicas})
