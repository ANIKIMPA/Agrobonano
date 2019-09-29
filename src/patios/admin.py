from django.contrib import admin
from .models import (
    Servicio,
    Imagen,
    Pagina,
    Cliente,
    Texto
)

# Register your models here.
class ServicioAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}

class PaginaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

class TextoAdmin(admin.ModelAdmin):
    list_display = ['pagina', 'posicion', 'texto']

admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Imagen)
admin.site.register(Pagina, PaginaAdmin)
admin.site.register(Cliente)
admin.site.register(Texto, TextoAdmin)
