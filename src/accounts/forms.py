# users/forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import password_validation
from .models import Usuario
from patios.models import Pagina, Imagen, Texto, Servicio, Cliente

class ContrasenaChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña antigua",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        strip=False,
    )
    new_password1 = forms.CharField(
        label="Contraseña nueva",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Contraseña nueva (confirmación)",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        strip=False,
    )

    class Meta(PasswordChangeForm):
        model = Usuario
        fields = "__all__"
        widgets = {
            'old_password': forms.PasswordInput(attrs={"class": "form-control"}),
            'new_password1': forms.PasswordInput(attrs={"class": "form-control"}),
            'new_password2': forms.PasswordInput(attrs={"class": "form-control"}),
        }

class UsuarioCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label="Contraseña (confirmación)",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        strip=False,
        help_text="Para verificar, introduzca la misma contraseña anterior.",
    )

    class Meta(UserCreationForm):
        model = Usuario
        fields = ('username', 'email')
        widgets = {
             'username': forms.TextInput(attrs={"class": "form-control"}),
             'email': forms.TextInput(attrs={"class": "form-control"}),
         }

class UsuarioChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label= ("Password"),
        help_text= (
            """Las contraseñas no se almacenan, por lo que no
            hay forma de ver la contraseña de este usuario"""
        ),
    )

    class Meta(UserChangeForm):
        model = Usuario
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control"}),
        }

class UsuarioAuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(AuthenticationForm):
        model = Usuario

class PageAdminForm(forms.ModelForm):
    titulo = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        textos = Texto.objects.filter(pagina=self.instance).order_by('posicion')
        
        for i in range(len(textos)):
            field_name = 'texto_%s' % (i + 1,)
            self.fields[field_name] = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
            self.initial[field_name] = textos[i].texto

        if self.instance.id != 1:
            self.fields['imagenes'] = forms.ModelMultipleChoiceField(required=False, queryset=Imagen.objects.filter(pagina=self.instance), widget=forms.SelectMultiple(attrs={'class': 'custom-select'}))
    # Finish __init__

    def save(self):
        pagina = self.instance
        pagina.titulo = self.cleaned_data["titulo"]
        pagina.descripcion = self.cleaned_data["descripcion"]
        pagina.save()

        textos = Texto.objects.filter(pagina=pagina).order_by('posicion')
        for i in range(len(textos)):
            field_name = 'texto_%s' % (i + 1,)
            textos[i].texto = self.cleaned_data[field_name]
            textos[i].save()
        
    class Meta:
        model = Pagina
        exclude = ['nombre', 'slug']

class ImagenAdminForm(forms.ModelForm):
    titulo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Imagen
        fields = ['titulo', 'imagen', 'ocultar']

class ServicioAdminForm(forms.ModelForm):
     class Meta:
         model = Servicio
         fields = ['nombre', 'slug', 'imagen', 'horas', 'precio', 'descripcion', 'ocultar']
         widgets = {
             'nombre': forms.TextInput(attrs={"class": "form-control"}),
             'slug': forms.TextInput(attrs={"class": "form-control", "readonly": True}),
             'horas': forms.NumberInput(attrs={"class": "form-control"}),
             'precio': forms.NumberInput(attrs={"class": "form-control", "step": 0.25}),
             'descripcion': forms.Textarea(attrs={"class": "form-control"}),
         }

class ClienteAdminForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['fecha_solicitud', ]
        widgets = {
            'nombre': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'telefono': forms.TextInput(attrs={"class": "form-control"}),
            'mensaje': forms.Textarea(attrs={"class": "form-control"}),
        }