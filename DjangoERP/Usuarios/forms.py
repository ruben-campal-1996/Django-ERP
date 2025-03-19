# Usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from Inventario.models import Producto

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'correo', 'telefono', 'password1', 'password2')  # Añadimos 'telefono'
        labels = {
            'nombre': 'Nombre completo',
            'correo': 'Correo electrónico',
            'telefono': 'Número de teléfono',
        }
        help_texts = {
            'correo': 'Este será el campo para iniciar sesión.',
            'telefono': 'Ejemplo: +1234567890',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'correo', 'telefono', 'rol', 'is_active', 'is_staff', 'is_superuser')  # Añadimos 'telefono'
        labels = {
            'nombre': 'Nombre completo',
            'correo': 'Correo electrónico',
            'telefono': 'Número de teléfono',
            'rol': 'Rol del usuario',
            'is_active': 'Usuario activo',
            'is_staff': 'Acceso al admin',
            'is_superuser': 'Superusuario',
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'imagen']  # Todos los campos editables

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminamos el campo username si no lo usamos
        if 'username' in self.fields:
            del self.fields['username']