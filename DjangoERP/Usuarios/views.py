from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, login, logout, authenticate  # Cambiamos User por get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioCreationForm
from .models import Usuario

User = get_user_model()  # Esto usa Usuarios.Usuario en lugar de django.contrib.auth.models.User

def is_admin(user):
    return user.is_authenticated and user.rol == 'Administrador'

def logistics_view(request):
    return render(request, 'Usuarios/Logistics.html')

def index(request):
    return render(request, 'Logistics.html')

def register_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            # Guardar el usuario con commit=False para modificar antes de guardar
            user = form.save(commit=False)
            user.rol = 'Cliente'  # Asignar el rol 'Cliente' por defecto
            user.save()  # Guardar en la base de datos
            print(f"Usuario guardado: {user.correo} con rol {user.rol}")  # Depuración
            messages.success(request, 'Cuenta creada con éxito. ¡Ya puedes iniciar sesión!')
            return redirect('usuarios:login')
        else:
            # Mostrar errores del formulario para depurar
            print("Errores del formulario:", form.errors)
            messages.error(request, 'Error al registrar el usuario. Revisa los campos.')
    else:
        form = UsuarioCreationForm()
    return render(request, 'Usuarios/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        if not username_or_email or not password:
            messages.error(request, "Por favor, ingrese tanto el nombre/correo como la contraseña.")
            return redirect('usuarios:login')

        # Intento 1: Autenticar directamente con el valor como correo
        user = authenticate(request, username=username_or_email, password=password)
        
        # Intento 2: Si falla y no parece un correo, buscar por nombre
        if not user and '@' not in username_or_email:
            try:
                user_obj = User.objects.get(nombre=username_or_email)
                user = authenticate(request, username=user_obj.correo, password=password)
            except User.DoesNotExist:
                user = None
        
        # Intento 3: Si falla y parece un correo, buscar por correo (redundante, pero para claridad)
        if not user and '@' in username_or_email:
            try:
                user_obj = User.objects.get(correo=username_or_email)
                user = authenticate(request, username=user_obj.correo, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)
            next_url = request.GET.get('next', 'logistics')
            messages.success(request, "Bienvenido de nuevo!")
            return redirect(next_url)
        else:
            messages.error(request, "Nombre o correo y/o contraseña incorrectos")
    return render(request, 'Usuarios/login.html')


def logout_view(request):
    logout(request)
    return redirect('logistics')


@login_required
def gestion_usuarios(request):
    usuarios = Usuario.objects.all()
    create_form = UsuarioCreationForm()
    roles = Usuario._meta.get_field('rol').choices

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            form = UsuarioCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuario creado exitosamente.')
            else:
                messages.error(request, 'Error al crear el usuario.')
            return redirect('usuarios:gestion_usuarios')
        
        elif action == 'edit':
            user_id = request.POST.get('user_id')
            usuario = Usuario.objects.get(id_usuario=user_id)
            usuario.nombre = request.POST.get('nombre')
            usuario.correo = request.POST.get('correo')
            usuario.rol = request.POST.get('rol')
            if request.POST.get('password1'):
                usuario.set_password(request.POST.get('password1'))
            usuario.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios:gestion_usuarios')
        
        elif action == 'delete':
            user_id = request.POST.get('user_id')
            try:
                usuario = Usuario.objects.get(id_usuario=user_id)
                usuario.delete()
                messages.success(request, 'Usuario eliminado exitosamente.')
            except Usuario.DoesNotExist:
                messages.error(request, 'El usuario no existe.')
            return redirect('usuarios:gestion_usuarios')

    return render(request, 'usuarios/gestion_usuarios.html', {
        'usuarios': usuarios,
        'create_form': create_form,
        'roles': roles,
    })

@login_required
def admin_create_user(request):
    if request.user.usuario.rol != 'administrador':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('logistics')
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        rol = request.POST.get('rol')
        if form.is_valid() and rol in dict(Usuario.ROLES):
            user = form.save()
            usuario, created = Usuario.objects.get_or_create(user=user, defaults={'rol': rol})
            if not created:
                usuario.rol = rol
                usuario.save()
            messages.success(request, f"Usuario {user.username} creado con éxito.")
            return redirect('usuarios:admin_manage_users')
    else:
        form = UsuarioCreationForm()
    return render(request, 'Usuarios/create_user.html', {'form': form, 'roles': Usuario.ROLES})

@login_required
def admin_manage_users(request):
    if request.user.usuario.rol != 'administrador':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('logistics')
    usuarios = Usuario.objects.filter(user__is_superuser=False)
    return render(request, 'Usuarios/manage_users.html', {'usuarios': usuarios, 'roles': Usuario.ROLES})

@login_required
def admin_edit_user(request, user_id):
    if request.user.usuario.rol != 'administrador':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('logistics')
    try:
        usuario = Usuario.objects.get(user__id=user_id)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('usuarios:admin_manage_users')
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST, instance=usuario.user)
        rol = request.POST.get('rol')
        if form.is_valid() and rol in dict(Usuario.ROLES):
            user = form.save(commit=False)
            if 'password1' in form.cleaned_data and form.cleaned_data['password1']:
                user.set_password(form.cleaned_data['password1'])
            user.save()
            usuario.rol = rol
            usuario.save()
            messages.success(request, f"Usuario {user.username} actualizado con éxito.")
            return redirect('usuarios:admin_manage_users')
    else:
        form = UsuarioCreationForm(instance=usuario.user)
    return render(request, 'admin/edit_user.html', {'form': form, 'usuario': usuario, 'roles': Usuario.ROLES})