# Inventario/urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.inventario_view, name='inventario'),
    path('pedidos/', views.pedidos_view, name='pedidos'),
    path('add_pedido/', views.add_pedido_view, name='add_pedido'),
    path('actualizar_estado_pedido/', views.actualizar_estado_pedido, name='actualizar_estado_pedido'),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('descargar_registro/', views.descargar_registro, name='descargar_registro'),
    path('descargar_inventario/', views.descargar_inventario, name='descargar_inventario'),
]