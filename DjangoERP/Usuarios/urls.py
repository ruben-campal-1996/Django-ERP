from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/create_user/', views.admin_create_user, name='admin_create_user'),
    path('admin/manage_users/', views.admin_manage_users, name='admin_manage_users'),
    path('admin/edit_user/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
]