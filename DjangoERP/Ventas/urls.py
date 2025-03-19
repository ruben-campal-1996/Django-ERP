# Ventas/urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.ventas_view, name='ventas'),
    path('buscar_clientes/', views.buscar_clientes, name='buscar_clientes'),
    path('cliente_detalle_json/', views.cliente_detalle_json, name='cliente_detalle_json'),
]