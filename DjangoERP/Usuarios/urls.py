from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('logistics/', views.logistics_view, name='logistics'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('gestion_usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('gestion_usuarios/create_user/', views.admin_create_user, name='admin_create_user'),
    path('gestion_usuarios/manage_users/', views.admin_manage_users, name='admin_manage_users'),
    path('gestion_usuarios/edit_user/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
]