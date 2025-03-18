from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Producto, MovimientoStock, Pedido, DetallePedido  # Añadimos DetallePedido
from .forms import ProductoForm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone
from datetime import timedelta
from django.db import models
import io
import logging
import json
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@login_required
def inventario_view(request):
    if request.user.rol != 'Encargado de inventario':
        return redirect('usuarios:logistics')
    productos = Producto.objects.all()
    form = ProductoForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'pedido':
            productos_ids = request.POST.getlist('productos[]')
            logger.info(f"Registrando pedido con productos: {productos_ids}")
            pedido = Pedido.objects.create()
            logger.info(f"Pedido creado con ID: {pedido.id_pedido}")
            try:
                for prod_id in productos_ids:
                    producto = Producto.objects.get(id_producto=prod_id)
                    cantidad = int(request.POST.get(f'cantidades[{prod_id}]'))
                    logger.info(f"Procesando {producto.nombre} con cantidad {cantidad}")
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
                        logger.info(f"Detalle guardado para {producto.nombre}")
                    else:
                        messages.error(request, f"Stock insuficiente para {producto.nombre}")
                        pedido.delete()
                        logger.info("Pedido eliminado por stock insuficiente")
                        return redirect('inventario:inventario')
                messages.success(request, 'Pedido registrado exitosamente.')
                logger.info("Pedido registrado con éxito")
                return redirect('inventario:pedidos')
            except Producto.DoesNotExist:
                messages.error(request, "Producto no encontrado.")
                pedido.delete()
                logger.error("Producto no encontrado")
                return redirect('inventario:inventario')
            except Exception as e:
                messages.error(request, f"Error al registrar el pedido: {str(e)}")
                pedido.delete()
                logger.error(f"Error: {str(e)}")
                return redirect('inventario:inventario')
        
        elif action == 'delete':
            product_id = request.POST.get('product_id')
            try:
                producto = Producto.objects.get(id_producto=product_id)
                producto.delete()
                messages.success(request, 'Producto eliminado exitosamente.')
            except Producto.DoesNotExist:
                messages.error(request, 'El producto no existe.')
            return redirect('inventario:inventario')
        
        elif action == 'pedido':
            productos_ids = request.POST.getlist('productos[]')
            # Crear un nuevo pedido
            pedido = Pedido.objects.create()
            try:
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
                        # Registrar el detalle del pedido
                        DetallePedido.objects.create(
                            pedido=pedido,
                            producto=producto,
                            cantidad=cantidad
                        )
                    else:
                        messages.error(request, f"Stock insuficiente para {producto.nombre}")
                        pedido.delete()  # Eliminar el pedido si falla
                        return redirect('inventario:inventario')
                messages.success(request, 'Pedido registrado exitosamente.')
                return redirect('inventario:pedidos')  # Redirigir a la lista de pedidos
            except Producto.DoesNotExist:
                messages.error(request, "Producto no encontrado.")
                pedido.delete()  # Eliminar el pedido si falla
                return redirect('inventario:inventario')
            except Exception as e:
                messages.error(request, f"Error al registrar el pedido: {str(e)}")
                pedido.delete()  # Eliminar el pedido si falla
                return redirect('inventario:inventario')
        
        elif action == 'add_stock':
            productos_ids = request.POST.getlist('productos[]')
            for prod_id in productos_ids:
                try:
                    producto = Producto.objects.get(id_producto=prod_id)
                    cantidad = int(request.POST.get(f'cantidades[{prod_id}]'))
                    producto.stock += cantidad
                    producto.save()
                    MovimientoStock.objects.create(
                        producto=producto,
                        tipo='entrada',
                        cantidad=cantidad,
                        usuario=request.user
                    )
                except Producto.DoesNotExist:
                    messages.error(request, "Producto no encontrado.")
                    return redirect('inventario:inventario')
            messages.success(request, 'Stock recibido exitosamente.')
            return redirect('inventario:inventario')

    return render(request, 'Inventario/Inventario.html', {
        'productos': productos,
        'form': form
    })

@login_required
def buscar_productos(request):
    if request.user.rol != 'Encargado de inventario':
        return JsonResponse([], safe=False)
    term = request.GET.get('term', '')
    productos = Producto.objects.filter(nombre__icontains=term)[:10]
    results = [{'id': p.id_producto, 'text': p.nombre} for p in productos]
    return JsonResponse(results, safe=False)

@login_required
def descargar_registro(request):
    if request.user.rol != 'Encargado de inventario':
        return redirect('usuarios:logistics')
    movimientos = MovimientoStock.objects.all().order_by('-fecha')
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Registro de Movimientos de Inventario", styles['Heading1']))
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
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="registro_movimientos.pdf"'
    return response

@login_required
def descargar_inventario(request):
    if request.user.rol != 'Encargado de inventario':
        return redirect('usuarios:logistics')
    productos = Producto.objects.all().order_by('id_producto')
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
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
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="registro_inventario.pdf"'
    return response

@login_required
def add_pedido_view(request):
    return render(request, 'Inventario/add_pedido.html')

@login_required
def pedidos_view(request):
    tres_dias_atras = timezone.now() - timedelta(days=3)
    pedidos = Pedido.objects.filter(
        models.Q(estado='en_proceso') | 
        models.Q(estado='finalizada', fecha__gte=tres_dias_atras)
    ).order_by('id_pedido')
    
    logger.info(f"Pedidos recuperados: {list(pedidos)}")  # Log para depurar

    # Calcular el precio total para cada pedido
    pedidos_con_precio = []
    for pedido in pedidos:
        total_precio = sum(
            detalle.producto.precio * detalle.cantidad 
            for detalle in pedido.detallepedido_set.all()
        )
        pedidos_con_precio.append({
            'pedido': pedido,
            'total_precio': total_precio
        })

    return render(request, 'Inventario/Pedidos.html', {'pedidos_con_precio': pedidos_con_precio})
@csrf_exempt
def actualizar_estado_pedido(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_pedido = data.get('id_pedido')
        nuevo_estado = data.get('nuevo_estado')
        try:
            pedido = Pedido.objects.get(id_pedido=id_pedido)
            pedido.estado = nuevo_estado
            pedido.save()
            return JsonResponse({'status': 'success'})
        except Pedido.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Pedido no encontrado'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})