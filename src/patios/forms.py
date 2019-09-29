from django import forms
from .models import Cliente
import re

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['fecha_solicitud']
        widgets = {
            'nombre': forms.TextInput(attrs={"class": "form-control", "placeholder": "Entre su nombre *"}),
            'email': forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Entre su email *",
                "aria-describedby": "emailHelp"
                }),
            'telefono': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Teléfono *"
                }),
            'mensaje': forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Mensaje",
                "cols": "30"
                }),
        }
    
    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"]
        if not re.search("\d{3}-\d{3}-\d{4}", telefono) and not re.search("\(\d{3}\)\d{3}-\d{4}", telefono) and not re.search("\d{10}", telefono) and not re.search("\(\d{3}\)\d{7}", telefono):
            raise forms.ValidationError("Por favor entre un teléfono válido.")
        return telefono
        