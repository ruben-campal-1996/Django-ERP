from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioCreationForm
from .models import Usuario

@login_required
def logistics_view(request):  # Cambiado de seegson_view a logistics_view
    username = request.user.username
    return render(request, 'Usuarios/Logistics.html', {'username': username})

def index(request):
    return render(request, 'Logistics.html')

def register_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada con éxito. ¡Ya puedes iniciar sesión!')
            return redirect('login')
    else:
        form = UsuarioCreationForm()
    return render(request, 'Usuarios/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        if not username_or_email or not password:
            messages.error(request, "Por favor, ingrese tanto el nombre de usuario/correo como la contraseña.")
            return redirect('login')
        user = None
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = None
        else:
            user = User.objects.filter(username=username_or_email).first()
        if user and user.check_password(password):
            login(request, user)
            messages.success(request, "Bienvenido de nuevo!")
            return redirect('logistics')  # Cambiado de 'Seegson' a 'logistics'
        else:
            messages.error(request, "Nombre de usuario o correo electrónico y/o contraseña incorrectos")
    return render(request, 'Usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('logistics')  # Ya estaba como 'Logistics', pero lo ajustamos a minúsculas por consistencia

@login_required
def admin_create_user(request):
    if request.user.usuario.rol != 'administrador':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('logistics')  # Ya estaba como 'Logistics', ajustado a minúsculas
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
            return redirect('admin_manage_users')
    else:
        form = UsuarioCreationForm()
    return render(request, 'Usuarios/create_user.html', {'form': form, 'roles': Usuario.ROLES})

@login_required
def admin_manage_users(request):
    if request.user.usuario.rol != 'administrador':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('Logistics')  # Mantengo 'ebyte' ya que no es 'Seegson'
    usuarios = Usuario.objects.filter(user__is_superuser=False)
    return render(request, 'Usuarios/manage_users.html', {'usuarios': usuarios, 'roles': Usuario.ROLES})

@login_required
def admin_edit_user(request, user_id):
    if request.user.usuario.rol != 'administrador':
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('Logistics')  # Mantengo 'ebyte' ya que no es 'Seegson'
    try:
        usuario = Usuario.objects.get(user__id=user_id)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('admin_manage_users')
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
            return redirect('admin_manage_users')
    else:
        form = UsuarioCreationForm(instance=usuario.user)
    return render(request, 'admin/edit_user.html', {'form': form, 'usuario': usuario, 'roles': Usuario.ROLES})