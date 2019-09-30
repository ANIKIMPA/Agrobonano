from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core import serializers
from .models import Usuario
from patios.models import (
    Pagina, Imagen, Servicio, Cliente
)

from .forms import (
    UsuarioCreationForm,
    UsuarioChangeForm,
    UsuarioAuthenticationForm,
    PageAdminForm,
    ImagenAdminForm,
    ServicioAdminForm,
    ContrasenaChangeForm,
    ClienteAdminForm,
)

# Create your views here.
@staff_member_required(login_url='accounts:login')
def index_page(request):
    paginas = Pagina.objects.all()
    context = {
        "paginas": paginas,
    }
    return render(request, "accounts/index.html", context)

def login_page(request):
    if request.user.is_staff:
        return redirect("accounts:index")

    form = UsuarioAuthenticationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
             username = request.POST['username']
             password = request.POST['password']
             user = authenticate(username=username, password=password)
             if user is not None:
                 login(request, user)
                 return redirect(".")
             else:
                messages.info(request, "Invalid username or password")

    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)

def logout_request(request):
    logout(request)
    return redirect("accounts:login")

@staff_member_required(login_url='accounts:login')
def admin_lista_usuarios(request):
    usuarios = Usuario.objects.all()

    context = {
        "items": usuarios,
        "field_names": ["username", "first_name", "last_name", "email"],
        "col_headers": ["Username", "Nombre", "Apellidos", "Email"]
    }

    return render(request, "accounts/usuarios-list.html", context)

@staff_member_required(login_url='accounts:login')
def admin_add_usuario(request):
    form = UsuarioCreationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("accounts:lista-usuarios")

    context = {
        "form": form,
        "title": "Añadir Usuario"
    }

    return render(request, "accounts/change-form.html", context)

@staff_member_required(login_url='accounts:login')
def admin_edit_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    form = UsuarioChangeForm(request.POST or None, instance=usuario)

    if request.method == "POST":
        if form.is_valid():
            if usuario_id != 1:
                form.save()
            return redirect("accounts:lista-usuarios")

    context = {
        "form": form,
        "obj": usuario
    }

    return render(request, "accounts/change-form.html", context)

@staff_member_required(login_url='accounts:login')
def admin_delete_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if usuario_id != 1:
        usuario.delete()

    return redirect("accounts:lista-usuarios")

@staff_member_required(login_url='accounts:login')
def admin_change_password(request):
    if request.method == 'POST':
        form = ContrasenaChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña restablecida correctamente!')
            messages.success(request, 'Por favor inicie sesión nuevamente')
            return redirect('accounts:logout')
    else:
        form = ContrasenaChangeForm(request.user)

    context = {
        "form": form,
        "title": "Cambio de Contraseña"
    }
    return render(request, 'accounts/change-form.html', context)


@staff_member_required(login_url='accounts:login')
def admin_change_form(request, pagina_slug):
    pagina = get_object_or_404(Pagina, slug=pagina_slug)
    form = PageAdminForm(request.POST or None, instance=pagina)
    imgForm = ImagenAdminForm()

    if request.method == "POST":
        if form.is_valid():
            try:
                imagenes = Imagen.objects.filter(pagina=pagina).exclude(pk__in=form.cleaned_data['imagenes'])
                for imagen in imagenes:
                    imagen.delete()
                form.save()
            except:
                form.save()

            return redirect("accounts:index")
    template_name = "accounts/pagina-change-form.html"
    servicios = None
    if pagina.id == 1:
        servicios = Servicio.objects.all()
        template_name= "accounts/servicios_pagina.html"

    context = {
        "form": form,
        "imgForm": imgForm,
        "pagina": pagina,
        "items": servicios,
        "field_names": ['nombre', 'horas', 'precio'],
    }
    return render(request, template_name, context)

@staff_member_required(login_url='accounts:login')
def admin_save_image(request, pagina_id):
    if request.method == "POST":
        form = ImagenAdminForm(request.POST, request.FILES)
        pagina = get_object_or_404(Pagina, pk=pagina_id)

        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            imagen = form.cleaned_data['imagen']
            ocultar = form.cleaned_data['ocultar']
            obj = Imagen.objects.create(titulo=titulo, imagen=imagen, ocultar=ocultar, pagina=pagina)

    return redirect("accounts:pagina", pagina.slug)

@staff_member_required(login_url='accounts:login')
def admin_add_servicio(request):
    form = ServicioAdminForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("accounts:pagina", "servicios")

    context = {
        "form": form,
        "title": "Añadir Servicio"
    }

    return render(request, "accounts/change-form.html", context)

@staff_member_required(login_url='accounts:login')
def admin_servicio_detail(request, servicio_slug):
    servicio = get_object_or_404(Servicio, slug=servicio_slug)
    form = ServicioAdminForm(request.POST or None, request.FILES or None, instance=servicio)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("accounts:pagina", "servicios")

    context = {
        "obj": servicio,
        "form": form
    }

    return render(request, "accounts/change-form.html", context)

@staff_member_required(login_url='accounts:login')
def admin_delete_servicio(request, servicio_slug):
    servicio = get_object_or_404(Servicio, slug=servicio_slug)
    servicio.delete()
    return redirect("accounts:pagina", "servicios")

@staff_member_required(login_url='accounts:login')
def admin_lista_clientes(request):
    clientes = Cliente.objects.all()
    context = {
        "items": clientes,
        "col_headers": ["nombre", "email", "teléfono", "fecha de solicitud"],
        "field_names": ["nombre", "email", "telefono", "fecha_solicitud"],
    }

    return render(request, "accounts/clientes-list.html", context)

@staff_member_required(login_url='accounts:login')
def admin_add_cliente(request):
    form = ClienteAdminForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("accounts:clientes")

    context = {
        "form": form,
        "title": "Añadir Cliente"
    }
    return render(request, "accounts/change-form.html", context)

@staff_member_required(login_url='accounts:login')
def admin_edit_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    form = ClienteAdminForm(request.POST or None, instance=cliente)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("accounts:clientes")

    context = {
        "form": form,
        "obj": cliente
    }

    return render(request, "accounts/change-form.html", context)

@staff_member_required(login_url='accounts:login')
def admin_delete_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    cliente.delete()
    return redirect("accounts:clientes")
