from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('logistics/', views.logistics_view, name='logistics'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('gestion_usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
]