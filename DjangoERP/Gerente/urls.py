from django.urls import path
from . import views

app_name = 'Gerente'
urlpatterns = [
    path('', views.gerente_view, name='gerente'),
    path('descargar_informes/', views.descargar_informes, name='descargar_informes'),
]