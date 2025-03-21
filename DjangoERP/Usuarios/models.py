# Usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    def _create_user(self, correo, password, **extra_fields):
        if not correo:
            raise ValueError('El campo correo es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(correo, password, **extra_fields)

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True')
        return self._create_user(correo, password, **extra_fields)

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Gerente', 'Gerente'),
        ('Empleado de ventas', 'Empleado de ventas'),
        ('Contable', 'Contable'),
        ('Encargado de inventario', 'Encargado de inventario'),
        ('Cliente', 'Cliente'),
    ]
    
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    correo = models.EmailField(max_length=200, unique=True)
    telefono = models.CharField(max_length=15, unique=True, blank=True, null=True)
    rol = models.CharField(max_length=30, choices=ROL_CHOICES, default='Cliente')
    #Tengo que poner este campo por temas de Django y sus configuraciones internas.
    username = models.CharField(max_length=150, unique=False, blank=True, null=True, default=None)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre