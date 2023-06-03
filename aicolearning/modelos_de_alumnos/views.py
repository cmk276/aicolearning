from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Estás viendo la vista de Modelos de Alumnos")