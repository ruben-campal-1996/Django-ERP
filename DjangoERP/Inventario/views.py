# Inventario/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Producto
from Usuarios.forms import ProductoForm

@login_required
def inventario_view(request):
    if request.user.usuario.rol != 'Encargado de inventario':
        return redirect('logistics')  # Cambiado de 'home' a 'logistics' para consistencia
    productos = Producto.objects.all()
    return render(request, 'Inventario/Inventario.html', {'productos': productos})

class AgregarProductoView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'Inventario/agregar_producto.html'
    success_url = reverse_lazy('inventario')

    def get(self, request, *args, **kwargs):
        if request.user.usuario.rol != 'Encargado de inventario':
            return redirect('logistics')  # Cambiado de 'home' a 'logistics'
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.usuario.rol != 'Encargado de inventario':
            return redirect('logistics')  # Cambiado de 'home' a 'logistics'
        return super().post(request, *args, **kwargs)
