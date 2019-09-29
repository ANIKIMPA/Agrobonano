from django.urls import path
from .views import (
    home_page,
    sobre_mi,
    servicios,
    galeria,
)

app_name = 'patios'
urlpatterns = [
    path('', home_page, name='home'),
    path('sobre-mi/', sobre_mi, name='sobre-mi'),
    path('servicios/', servicios, name='servicios'),
    path('galeria/', galeria, name='galeria'),
]