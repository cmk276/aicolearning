#importaciones
import pandas as pd
from .models import DefinicionModelo, Caracteristica
from django import forms
    

#clase para un formulario que recibe un nombre de modelo y un fichero csv
class FormImportarModelo(forms.Form):
    nombre_modelo = forms.CharField(label="Nombre del modelo", widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={'class': 'form-control'}))
    fichero_csv = forms.FileField(label="Archivo CSV", widget=forms.FileInput(attrs={'class': 'form-control'}))

    def validar_nombre_modelo(self):
        nombre_modelo = self.cleaned_data['nombre_modelo']
        if DefinicionModelo.objects.filter(nombre=nombre_modelo).exists():
            raise forms.ValidationError("Ya existe un modelo con ese nombre")
        return nombre_modelo
    
    def validar_fichero_csv(self):
        fichero_csv = self.cleaned_data['fichero_csv']
        if not fichero_csv.name.endswith('.csv'):
            raise forms.ValidationError("El fichero no es un csv")
        return fichero_csv
    
    #validar los datos del formulario
    def clean(self):
        cleaned_data = super().clean()
        nombre_modelo = self.validar_nombre_modelo()
        fichero_csv = self.validar_fichero_csv()
        return cleaned_data
    