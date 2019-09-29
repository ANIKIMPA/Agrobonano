from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.
class Imagen(models.Model):
    titulo = models.CharField(max_length=50, unique=True)
    imagen = models.ImageField(upload_to='patios/images/')
    ocultar = models.BooleanField("Ocultar en site", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    pagina = models.ForeignKey('Pagina', on_delete=models.CASCADE)

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'

    def __str__(self):
        return self.titulo

class Pagina(models.Model):
    nombre = models.CharField(max_length=30)
    slug = models.CharField(max_length=30, unique=True)
    titulo = models.CharField("Título", max_length=30)
    descripcion = models.TextField("Descripción", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("accounts:pagina", args=[self.slug])

class Texto(models.Model):
    texto = models.TextField()
    posicion = models.IntegerField()
    pagina = models.ForeignKey('Pagina', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pagina', 'posicion']
        unique_together = ['pagina', 'posicion']

    def __str__(self):
        return self.texto
    

class Servicio(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=40, unique= True)
    imagen = models.ImageField(upload_to='patios/servicios/', null=True, blank=True)
    horas = models.CharField("Horas de trabajo", max_length=60, null=True, blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
    descripcion = models.TextField("Descripción", blank=True)
    ocultar = models.BooleanField("Ocultar en mi site", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("accounts:servicio-detail", args=[self.slug])

    def get_delete_url(self):
        return reverse("accounts:delete-servicio", args=[self.slug])
    

class Cliente(models.Model):
    nombre = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=16)
    mensaje = models.TextField(null=True, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("accounts:edit-cliente", kwargs={"cliente_id": self.pk})
    
    def get_delete_url(self):
        return reverse("accounts:delete-cliente", args=[self.id])