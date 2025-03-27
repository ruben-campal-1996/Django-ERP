from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from Contabilidad.models import Budget, Transaccion
from Inventario.models import Producto, MovimientoStock
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io
import zipfile
from datetime import datetime, timedelta

@login_required
def gerente_view(request):
    if request.user.rol != 'Gerente':
        return redirect('usuarios:logistics')
    return render(request, 'Gerente/gerente.html', {})

@login_required
def descargar_informes(request):
    if request.user.rol != 'Gerente':
        return redirect('usuarios:logistics')

    # Obtener el período desde el parámetro GET
    periodo = request.GET.get('periodo', '7d')
    if periodo == '24h':
        delta = timedelta(hours=24)
    elif periodo == '3d':
        delta = timedelta(days=3)
    else:  # '7d'
        delta = timedelta(days=7)
    
    fecha_limite = timezone.now() - delta

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Historial de transacciones
        budget = Budget.objects.first()
        transacciones = Transaccion.objects.filter(budget=budget, fecha__gte=fecha_limite).order_by('-fecha')
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
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
        pdf_buffer.seek(0)
        zip_file.writestr('historial_transacciones.pdf', pdf_buffer.getvalue())

        # Registro de inventario (sin filtro de fecha)
        productos = Producto.objects.all().order_by('id_producto')
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        centered_style = styles['Heading1']
        centered_style.alignment = 1
        elements.append(Paragraph("Registro de Inventario", centered_style))
        data = [['ID', 'Nombre', 'Precio', 'Stock']]
        for prod in productos:
            data.append([
                prod.id_producto,
                prod.nombre,
                f"${prod.precio}",
                prod.stock
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
        pdf_buffer.seek(0)
        zip_file.writestr('registro_inventario.pdf', pdf_buffer.getvalue())

        # Registro de movimientos
        movimientos = MovimientoStock.objects.filter(fecha__gte=fecha_limite).order_by('-fecha')
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph(f"Registro de Movimientos de Inventario (Últimos {periodo})", styles['Heading1']))
        data = [['ID', 'Producto', 'Tipo', 'Cantidad', 'Fecha', 'Usuario']]
        for mov in movimientos:
            usuario = mov.usuario.nombre if mov.usuario else 'N/A'
            data.append([
                mov.id,
                mov.producto.nombre,
                mov.tipo.capitalize(),
                mov.cantidad,
                mov.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                usuario
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
        pdf_buffer.seek(0)
        zip_file.writestr('registro_movimientos.pdf', pdf_buffer.getvalue())

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="informes_{timestamp}.zip"'
    return response