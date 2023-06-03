from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Gestionando el centro de estudios")

# Create your views here.
