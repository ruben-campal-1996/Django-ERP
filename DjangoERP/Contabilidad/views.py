from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from .models import Budget, Transaccion


@login_required
def contabilidad_dashboard(request):
    budget = Budget.objects.first() 
    if not budget:
        budget = Budget.objects.create()
    
    # Obtener todas las transacciones y ordenarlas por fecha descendente
    transacciones_list = Transaccion.objects.filter(budget=budget).order_by('-fecha')
    
    # Configurar el paginador: 10 transacciones por página
    paginator = Paginator(transacciones_list, 7)
    page_number = request.GET.get('page')
    transacciones = paginator.get_page(page_number)
    
    # Calcular totales
    ingresos_totales = transacciones_list.filter(tipo='ingreso').aggregate(total=models.Sum('monto'))['total'] or 0
    egresos_totales = transacciones_list.filter(tipo='egreso').aggregate(total=models.Sum('monto'))['total'] or 0
    saldo_total = budget.monto
    ganancias_perdidas = ingresos_totales - egresos_totales

    context = {
        'budget': budget,
        'transacciones': transacciones,  # Ahora es un objeto paginado
        'ingresos_totales': ingresos_totales,
        'egresos_totales': egresos_totales,
        'ganancias_perdidas': ganancias_perdidas,
        'saldo_total': saldo_total,
    }
    return render(request, 'contabilidad/contabilidad.html', context)

