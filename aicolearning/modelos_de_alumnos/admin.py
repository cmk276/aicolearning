'''
AICoLearning
Herramienta web para la creación de grupos colaborativos asistida por Machine Learning
Código desarrollado por: Francisco Tejeira Bújez
Para el Proyecto fin de Grado de Ingeniería Informática de la UNIR
2023
'''
from django.contrib import admin

# Register your models here.
from .models import DefinicionModelo, Caracteristica, ValorSeleccion

class CaracteristicaInline(admin.TabularInline):
    model = Caracteristica
    extra = 3

class DefinicionModeloAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["nombre"]})
    ]

    inlines = [CaracteristicaInline]

admin.site.register(DefinicionModelo, DefinicionModeloAdmin)

class ValorSeleccionInline(admin.StackedInline):
    model = ValorSeleccion
    extra = 3

class DefinicionCaracteristicaAdmin(admin.ModelAdmin):
    inlines = [ValorSeleccionInline]

admin.site.register(Caracteristica, DefinicionCaracteristicaAdmin)
