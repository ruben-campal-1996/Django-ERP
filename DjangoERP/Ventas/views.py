# Ventas/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from Usuarios.models import Usuario
from Usuarios.forms import UsuarioCreationForm

@login_required
def ventas_view(request):
    if request.user.rol != 'Empleado de ventas':
        return redirect('usuarios:logistics')
    
    # Búsqueda y filtrado
    search_term = request.GET.get('search', '')
    clientes_list = Usuario.objects.filter(rol='Cliente', is_superuser=False)
    if search_term:
        clientes_list = clientes_list.filter(
            Q(nombre__icontains=search_term) |
            Q(correo__icontains=search_term) |
            Q(telefono__icontains=search_term)
        )
    
    # Paginación
    clientes_list = clientes_list.order_by('id_usuario')
    paginator = Paginator(clientes_list, 10)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)
    
    # Formulario para crear clientes
    form = UsuarioCreationForm()
    if request.method == 'POST':
        if 'create_cliente' in request.POST:
            form = UsuarioCreationForm(request.POST)
            if form.is_valid():
                usuario = form.save(commit=False)
                usuario.rol = 'Cliente'
                usuario.save()
                messages.success(request, 'Cliente creado exitosamente.')
                return redirect('ventas:ventas')
            else:
                messages.error(request, 'Error al crear el cliente. Revisa los datos.')
        
        elif 'create_pedido' in request.POST:
            cliente_id = request.POST.get('cliente')
            productos_ids = request.POST.getlist('productos[]')
            descripcion = request.POST.get('descripcion', '')
            try:
                cliente = Usuario.objects.get(id_usuario=cliente_id, rol='Cliente') if cliente_id else None
                pedido = Pedido.objects.create(descripcion=descripcion, cliente=cliente)
                for prod_id in productos_ids:
                    producto = Producto.objects.get(id_producto=prod_id)
                    cantidad = int(request.POST.get(f'cantidades[{prod_id}]'))
                    if producto.stock >= cantidad:
                        producto.stock -= cantidad
                        producto.save()
                        MovimientoStock.objects.create(
                            producto=producto,
                            tipo='salida',
                            cantidad=cantidad,
                            usuario=request.user
                        )
                        DetallePedido.objects.create(
                            pedido=pedido,
                            producto=producto,
                            cantidad=cantidad
                        )
                    else:
                        messages.error(request, f"Stock insuficiente para {producto.nombre}")
                        pedido.delete()
                        return redirect('ventas:ventas')
                messages.success(request, 'Pedido registrado exitosamente.')
                return redirect('ventas:ventas')
            except Exception as e:
                messages.error(request, f"Error al registrar el pedido: {str(e)}")
                return redirect('ventas:ventas')
    
    return render(request, 'Ventas/ventas.html', {
        'clientes': clientes,
        'form': form,
        'search_term': search_term
    })

@login_required
def cliente_detalle_view(request, id_usuario):
    if request.user.rol != 'Empleado de ventas':
        return redirect('usuarios:logistics')
    try:
        cliente = Usuario.objects.get(id_usuario=id_usuario, rol='Cliente', is_superuser=False)
        return render(request, 'Ventas/cliente_detalle.html', {'cliente': cliente})
    except Usuario.DoesNotExist:
        messages.error(request, 'Cliente no encontrado.')
        return redirect('ventas:ventas')

@login_required
def buscar_clientes(request):
    if request.user.rol != 'Empleado de ventas':
        return JsonResponse([], safe=False)
    term = request.GET.get('term', '')
    clientes = Usuario.objects.filter(rol='Cliente', is_superuser=False, nombre__icontains=term)[:10]
    results = [{'id': str(c.id_usuario), 'text': c.nombre} for c in clientes]
    print(f"Clientes encontrados: {results}")  # Depuración
    return JsonResponse(results, safe=False)