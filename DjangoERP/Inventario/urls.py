from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.inventario_view, name='inventario'),
    path('agregar/', views.AgregarProductoView.as_view(), name='agregar_producto'),
]