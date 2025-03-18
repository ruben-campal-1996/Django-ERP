# Inventario/urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.inventario_view, name='inventario'),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('descargar_registro/', views.descargar_registro, name='descargar_registro'),
    path('descargar_inventario/', views.descargar_inventario, name='descargar_inventario'),
]