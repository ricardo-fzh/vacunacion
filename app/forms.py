from django import forms
from .models import Hora, Persona, Centro
from .helper import digito_verificador

class HorasForm(forms.ModelForm):
    class Meta:
        model =  Hora
        fields = '__all__'
        widgets = {
        'hora': forms.TextInput(attrs={'type': 'time'}),
        'dia': forms.TextInput(attrs={'type': 'date'})
        }



    
class PersonaForm(forms.ModelForm):
    class  Meta:
        model =  Persona
        fields = '__all__'
        exclude = ['vacuna_disponible', 'centros','horas', 'horas_seg_v', 'fecha_seg_vacunacion']
        widgets = {
        'fecha_nac': forms.TextInput(attrs={'type': 'date'}),
        'celular': forms.TextInput(attrs={'placeholder': '+569xxxxxxxx'}),
        'direccion' :forms.TextInput(attrs={'placeholder': 'Ej: Los Aromos 3339, Renca'})
        }
    
    #Validaciones se debe validar el rut si existe y es correcto   

            
    def clean_dv(self):
        rut = self.cleaned_data.get('rut')
        dv_valido = digito_verificador(rut)
        dv = self.cleaned_data.get('dv')
        
        if str(dv) != str(dv_valido):
            raise forms.ValidationError("El R.U.T es incorrecto")
        return dv
    
    def clean_nombre(self):
        nombre = " ".join(self.cleaned_data.get('nombre').split())
        return nombre.title()

    def clean_apellido_materno(self):
        apellido_materno = " ".join(self.cleaned_data.get('apellido_materno').split())
        return apellido_materno.title()

    def clean_apellido_paterno(self):
        apellido_paterno = " ".join(self.cleaned_data.get('apellido_paterno').split())
        return apellido_paterno.title()