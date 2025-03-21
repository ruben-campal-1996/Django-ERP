from django.shortcuts import get_object_or_404, render, redirect
from Inventario.models import Pedido
from django.contrib.auth.decorators import login_required
from .models import Budget, Transaccion

@login_required
def contabilidad_view(request):
    if request.user.rol != 'Contable':
        return redirect('usuarios:logistics')
    
    budget = Budget.objects.first()  # Asumimos un solo budget por ahora
    transacciones = Transaccion.objects.all().order_by('-fecha')
    
    return render(request, 'Contabilidad/contabilidad.html', {
        'budget': budget,
        'transacciones': transacciones
    })

def crear_transaccion_segun_rol(pedido):
    if Transaccion.objects.filter(pedido=pedido).exists():
        return  # Evitar duplicados

    monto = sum(
        detalle.producto.precio * detalle.cantidad
        for detalle in pedido.detallepedido_set.all()
    )
    
    budget = Budget.objects.first()
    if not budget:
        budget = Budget.objects.create()

    rol = pedido.cliente.rol
    if rol == 'Encargado de inventario':
        tipo = 'egreso'
        descripcion = f"Gasto por pedido {pedido.id_pedido} (reabastecimiento)"
    elif rol in ['Cliente', 'Empleado de ventas']:
        tipo = 'ingreso'
        descripcion = f"Ingreso por pedido {pedido.id_pedido} (venta)"
    else:
        return

    Transaccion.objects.create(
        budget=budget,
        tipo=tipo,
        monto=monto,
        descripcion=descripcion,
        pedido=pedido
    )

def contabilidad_dashboard(request):
    """
    Vista para el dashboard de Contabilidad.
    Muestra el saldo del budget y la lista de transacciones.
    """
    # Obtener o crear el budget
    budget = Budget.objects.first()
    if not budget:
        budget = Budget.objects.create()

    # Obtener todas las transacciones asociadas al budget
    transacciones = Transaccion.objects.filter(budget=budget).order_by('-fecha')

    context = {
        'budget': budget,
        'transacciones': transacciones,
    }
    return render(request, 'contabilidad/contabilidad_dashboard.html', context)


