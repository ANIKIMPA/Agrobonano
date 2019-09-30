from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
import re
from .forms import ClientesForm
from .models import (
    Servicio,
    Pagina,
    Texto,
    Imagen,
    Cliente
)

# Create your views here.
def home_page(request):
    pagina_inicio = None
    # pagina_inicio = get_object_or_404(Pagina, pk=2)
    context = get_context(request, pagina_inicio)
    return send_email_or_render(request, "patios/home.html", context)
    

def sobre_mi(request):
    pagina_sobre_mi = get_object_or_404(Pagina, pk=3)
    context = get_context(request, pagina_sobre_mi)
    return send_email_or_render(request, "patios/sobre-mi.html", context)

def servicios(request):
    pagina_servicios = get_object_or_404(Pagina, pk=1)
    servicios = Servicio.objects.filter(ocultar=False)
    context = {
        'pagina': pagina_servicios,
        'servicios': servicios
    }
    context.update(get_contacto_context(request))
    
    return send_email_or_render(request, "patios/servicios.html", context)

def galeria(request):
    pagina_galeria = get_object_or_404(Pagina, pk=4)

    imagenes_prueba = [
        "https://images.pexels.com/photos/62307/air-bubbles-diving-underwater-blow-62307.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "https://images.pexels.com/photos/38238/maldives-ile-beach-sun-38238.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "https://images.pexels.com/photos/158827/field-corn-air-frisch-158827.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "https://images.pexels.com/photos/302804/pexels-photo-302804.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "https://images.pexels.com/photos/1038914/pexels-photo-1038914.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "https://images.pexels.com/photos/414645/pexels-photo-414645.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
        "https://images.pexels.com/photos/56005/fiji-beach-sand-palm-trees-56005.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "https://images.pexels.com/photos/1038002/pexels-photo-1038002.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
    ]
    con = {
        "imgs": imagenes_prueba
    }
    context = get_context(request, pagina_galeria)
    context.update(con)

    return send_email_or_render(request, "patios/galeria.html", context)

def get_context(request, pagina):
    textos = Texto.objects.filter(pagina_id=pagina.id)
    imagenes = Imagen.objects.filter(pagina_id=pagina.id, ocultar=False)
    context = {
        "pagina": pagina,
        "textos": textos,
        "imagenes": imagenes,
    }
    context.update(get_contacto_context(request))

    return context

def get_contacto_context(request):
    pagina_contacto = get_object_or_404(Pagina, pk=5)
    textos = Texto.objects.filter(pagina_id=5)
    imagenes = Imagen.objects.filter(pagina_id=5, ocultar=False)
    form = ClientesForm(request.POST or None)

    context = {
        "form": form,
        "pagina_contacto": pagina_contacto,
        "textos_contacto": textos,
        "imagenes_contacto": imagenes,
        "ws_num": re.sub('[^0-9]', '', textos[1].texto)
    }
    return context

def send_email_or_render(request, template_name, context):
    if request.method == "POST":
        form = ClientesForm(request.POST)
        if form.is_valid():
            nombre = request.POST.get('nombre')
            from_email = request.POST.get('email')
            message = request.POST.get('mensaje')

            # Convertir telefono a formato ###-###-####
            telefono = request.POST.get('telefono')
            telefono = telefono.replace("(", "")
            telefono = telefono.replace(")", "")
            telefono = telefono.replace("-", "")
            telefono = telefono[:3] + "-" + telefono[3:6] + "-" + telefono[6:]

            try:
                send_mail(
                        f'Mensaje de {nombre}',
                        f'Telefono: {telefono}\n\n{message}',
                        from_email,
                        ['niovan.martinez9@gmail.com'],
                        fail_silently=False
                    )
                cliente = Cliente.objects.create(nombre=nombre, email=from_email, telefono=telefono, mensaje=message)
            except BadHeaderError:
                messages.error(request, "Hubo un error")
            
            return redirect("patios:home")
        else:
            messages.error(request, "Arregle los siguientes errores:")
            context.update({ "anchor": "contacto"})

    return render(request, template_name, context)

  