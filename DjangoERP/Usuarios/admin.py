# Usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm

class CustomUserAdmin(UserAdmin):
    # Formularios personalizados
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    
    # Campos a mostrar en la lista de usuarios
    list_display = ('id_usuario', 'nombre', 'correo', 'rol', 'is_staff', 'is_superuser')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('nombre', 'correo')
    
    # Campos al crear un usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre', 'correo', 'rol', 'password1', 'password2'),
        }),
    )
    
    # Campos al editar un usuario
    fieldsets = (
        (None, {'fields': ('nombre', 'correo', 'password')}),
        ('Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Ordenamiento por defecto
    ordering = ('id_usuario',)

# Registramos el modelo con la configuración personalizada
admin.site.register(Usuario, CustomUserAdmin)