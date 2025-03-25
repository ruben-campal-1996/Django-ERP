from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Budget, Transaccion

@login_required
def contabilidad_dashboard(request):
    """
    Vista para el dashboard de Contabilidad.
    Muestra el saldo del budget, la lista de transacciones y las ganancias/pérdidas.
    """
    # Obtener o crear el budget
    budget = Budget.objects.first()
    if not budget:
        budget = Budget.objects.create()

    # Obtener todas las transacciones asociadas al budget
    transacciones = Transaccion.objects.filter(budget=budget).order_by('-fecha')

    # Calcular ingresos y egresos totales
    ingresos_totales = transacciones.filter(tipo='ingreso').aggregate(total=models.Sum('monto'))['total'] or 0
    egresos_totales = transacciones.filter(tipo='egreso').aggregate(total=models.Sum('monto'))['total'] or 0
    ganancias_perdidas = ingresos_totales - egresos_totales

    context = {
        'budget': budget,
        'transacciones': transacciones,
        'ingresos_totales': ingresos_totales,
        'egresos_totales': egresos_totales,
        'ganancias_perdidas': ganancias_perdidas,
    }
    return render(request, 'contabilidad/contabilidad.html', context)

