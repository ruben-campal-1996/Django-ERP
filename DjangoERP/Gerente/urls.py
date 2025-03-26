from django.urls import path
from . import views

app_name = 'Gerente'
urlpatterns = [
    path('', views.gerente_view, name='gerente'),
]