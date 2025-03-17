# Inventario/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm

@login_required
def inventario_view(request):
    if request.user.usuario.rol != 'Encargado de inventario':
        return redirect('logistics')
    productos = Producto.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete':
            product_id = request.POST.get('product_id')
            try:
                producto = Producto.objects.get(id_producto=product_id)
                producto.delete()
                messages.success(request, 'Producto eliminado exitosamente.')
            except Producto.DoesNotExist:
                messages.error(request, 'El producto no existe.')
            return redirect('inventario:inventario')

    return render(request, 'Inventario/Inventario.html', {
        'productos': productos
    })

class AgregarProductoView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'Inventario/agregar_producto.html'
    success_url = reverse_lazy('inventario:inventario')

    def get(self, request, *args, **kwargs):
        if request.user.usuario.rol != 'Encargado de inventario':
            return redirect('logistics')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.usuario.rol != 'Encargado de inventario':
            return redirect('logistics')
        return super().post(request, *args, **kwargs)