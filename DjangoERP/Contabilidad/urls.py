from django.urls import path
from django.conf import settings  # Añade esta línea
from django.conf.urls.static import static  # Ya deberías tener esta línea
from . import views

app_name = 'contabilidad'

urlpatterns = [
    path('', views.contabilidad_dashboard, name='contabilidad'),
]