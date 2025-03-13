from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.logistics_view, name='logistics'),  # Página de inicio
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

]