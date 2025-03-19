# Ventas/urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.ventas_view, name='ventas'),
    path('cliente/<int:id_usuario>/', views.cliente_detalle_view, name='cliente_detalle'),
    path('buscar_clientes/', views.buscar_clientes, name='buscar_clientes'),
]