from django import forms
from .trabajo_colaborativo_utiles import TIPOS_AGRUPAMIENTO

# Form que recibe un nombre de modelo de alumno para el que se va a configurar el agrupamiento
# Recibe una lista de características formadas por una etiqueta y valor que se pueden seleccionar
# y permite elegir entre agrupamiento aleatorio, homogéneo y heterogéneo

class FormConfigurarAgrupamiento(forms.Form):
    
    alumnos_por_grupo = forms.IntegerField(required=True, label="Número de alumnos por grupo")
    caracteristicas = forms.MultipleChoiceField(choices=[], 
        widget=forms.CheckboxSelectMultiple, required=True, label="Seleccione al menos una característica:"
    )
    tipo_agrupamiento = forms.ChoiceField(choices=TIPOS_AGRUPAMIENTO, required=True, label="Tipo de agrupamiento", widget=forms.RadioSelect)
    
# validar formulario
    def clean(self):
        cleaned_data = super().clean()
        alumnos_por_grupo = cleaned_data.get("alumnos_por_grupo")
        tipo_agrupamiento = cleaned_data.get("tipo_agrupamiento")
        caracteristicas = cleaned_data.get("caracteristicas")
        
        print("\nVALIDANDO CARACTERISTICAS: ", caracteristicas)

        if alumnos_por_grupo is None:
            raise forms.ValidationError("Debe introducir un número de alumnos por grupo")
        if caracteristicas is None:
            raise forms.ValidationError("Debe seleccionar al menos una característica")
        if tipo_agrupamiento is None:
            raise forms.ValidationError("Debe seleccionar un tipo de agrupamiento")
        return cleaned_data

    