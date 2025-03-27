from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone
from .models import Budget, Transaccion
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta
import io


@login_required
def contabilidad_dashboard(request):
    if request.user.rol not in ['Contable', 'Gerente']:
        return redirect('usuarios:logistics')
    
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

@login_required
def descargar_movimientos(request):
    if request.user.rol not in ['Contable', 'Gerente']:
        return redirect('usuarios:logistics')

    budget = Budget.objects.first()
    # Obtener el período desde el parámetro GET
    periodo = request.GET.get('periodo', '7d')
    if periodo == '24h':
        delta = timedelta(hours=24)
    elif periodo == '3d':
        delta = timedelta(days=3)
    else:  # '7d'
        delta = timedelta(days=7)
    
    fecha_limite = timezone.now() - delta
    transacciones = Transaccion.objects.filter(budget=budget, fecha__gte=fecha_limite).order_by('-fecha')
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Historial de Transacciones (Últimos {periodo})", styles['Heading1']))
    
    data = [['ID', 'Tipo', 'Monto', 'Descripción', 'Fecha', 'Pedido']]
    for trans in transacciones:
        pedido = trans.pedido.id_pedido if trans.pedido else 'N/A'
        data.append([
            trans.id,
            trans.tipo.capitalize(),
            f"${trans.monto}",
            trans.descripcion,
            trans.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            pedido
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historial_transacciones.pdf"'
    return response

