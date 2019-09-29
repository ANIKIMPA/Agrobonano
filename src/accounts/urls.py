from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    login_page, logout_request, index_page,
    admin_change_form, admin_save_image,
    admin_servicio_detail,
    admin_add_servicio,
    admin_delete_servicio,
    admin_lista_usuarios,
    admin_add_usuario,
    admin_edit_usuario,
    admin_delete_usuario,
    admin_change_password,
    admin_lista_clientes,
    admin_edit_cliente,
    admin_add_cliente,
    admin_delete_cliente,
)

app_name = 'accounts'
urlpatterns = [
    path('', index_page, name='index'),
    path('login/', login_page, name='login'),
    path('logout/', logout_request, name='logout'),


    path('view/usuarios/', admin_lista_usuarios, name='lista-usuarios'),
    path('usuarios/add-new/', admin_add_usuario, name='add-usuario'),
    path('usuarios/edit/<int:usuario_id>/', admin_edit_usuario, name='edit-usuario'),
    path('usuarios/delete/<int:usuario_id>/', admin_delete_usuario, name='delete-usuario'),
    path('usuarios/edit/password/', admin_change_password, name='change-password'),

    path('servicios/add-new/', admin_add_servicio, name='add-servicio'),
    path('servicios/edit/<servicio_slug>/', admin_servicio_detail, name='servicio-detail'),
    path('servicios/delete/<servicio_slug>/', admin_delete_servicio, name='delete-servicio'),


    path('view/clientes/', admin_lista_clientes, name='clientes'),
    path('clientes/add-new/', admin_add_cliente, name='add-cliente'),
    path('clientes/edit/<int:cliente_id>/', admin_edit_cliente, name='edit-cliente'),
    path('clientes/delete/<int:cliente_id>/', admin_delete_cliente, name='delete-cliente'),

    path('view/<pagina_slug>/', admin_change_form, name='pagina'),
    path('admin_save_image/<int:pagina_id>/', admin_save_image, name='save-image'),
]
