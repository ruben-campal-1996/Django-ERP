from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Choices para el campo Rol
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Gerente', 'Gerente'),
        ('Empleado de ventas', 'Empleado de ventas'),
        ('Contable', 'Contable'),
        ('Encargado de inventario', 'Encargado de inventario'),
        ('Cliente', 'Cliente'),
    ]
    
    # Campos personalizados
    id_usuario = models.AutoField(primary_key=True)  # Llave primaria autoincremental
    nombre = models.CharField(max_length=150)  # VARCHAR(150)
    correo = models.EmailField(max_length=200, unique=True)  # VARCHAR(200), único
    rol = models.CharField(max_length=30, choices=ROL_CHOICES, default='Cliente')
    
    # Sobrescribimos el campo username para que no sea obligatorio si usamos correo
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    
    # Indicamos qué campo se usará para iniciar sesión (correo en lugar de username)
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']  # Campos requeridos al crear un usuario

    def __str__(self):
        return self.nombre
