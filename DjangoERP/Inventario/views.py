from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Producto, MovimientoStock, Pedido, DetallePedido
from .forms import ProductoForm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from Contabilidad.models import Budget, Transaccion
from decimal import Decimal
import io
import logging
import json 

logger = logging.getLogger(__name__)

@login_required
def inventario_view(request):
    if request.user.rol != 'Encargado de inventario':
        return redirect('usuarios:logistics')
    
    search_term = request.GET.get('search', '')
    productos_list = Producto.objects.all()
    if search_term:
        productos_list = productos_list.filter(
            Q(nombre__icontains=search_term) | Q(id_producto__icontains=search_term)
        )
    
    productos_list = productos_list.order_by('id_producto')
    paginator = Paginator(productos_list, 10)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    form = ProductoForm()
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto creado exitosamente.')
                return redirect('inventario:inventario')
            else:
                messages.error(request, 'Error al crear el producto.')
        
        elif action == 'edit':
            product_id = request.POST.get('product_id')
            try:
                producto = Producto.objects.get(id_producto=product_id)
                producto.nombre = request.POST.get('nombre')
                producto.descripcion = request.POST.get('descripcion')
                producto.precio = request.POST.get('precio')
                producto.stock = request.POST.get('stock')
                if 'imagen' in request.FILES:
                    producto.imagen = request.FILES['imagen']
                producto.save()
                messages.success(request, 'Producto actualizado exitosamente.')
            except Producto.DoesNotExist:
                messages.error(request, 'El producto no existe.')
            except Exception as e:
                messages.error(request, f'Error al editar el producto: {str(e)}')
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
            descripcion = request.POST.get('descripcion', '')
            logger.info(f"Registrando pedido con productos: {productos_ids}")
            pedido = Pedido.objects.create(descripcion=descripcion, cliente=request.user)
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
                monto_base = sum(
                    detalle.producto.precio * detalle.cantidad
                    for detalle in pedido.detallepedido_set.all()
                )
                logger.info(f"Monto base calculado: {monto_base}")
                if pedido.cliente.rol == 'Encargado de inventario':
                    monto = monto_base * Decimal('0.75')
                    logger.info(f"Rol: {pedido.cliente.rol}, Monto con descuento (25%): {monto}")
                else:
                    monto = monto_base
                    logger.info(f"Rol: {pedido.cliente.rol}, Monto sin descuento: {monto}")
                
                budget = Budget.objects.first()
                if not budget:
                    budget = Budget.objects.create()
                rol = pedido.cliente.rol
                if rol == 'Encargado de inventario':
                    tipo = 'egreso'
                    descripcion_trans = f"Gasto por pedido {pedido.id_pedido} (reabastecimiento, 25% descuento)"
                elif rol in ['Cliente', 'Empleado de ventas']:
                    tipo = 'ingreso'
                    descripcion_trans = f"Ingreso por pedido {pedido.id_pedido} (venta)"
                else:
                    tipo = None
                if tipo:
                    logger.info(f"Creando transacción: {tipo} - Monto: {monto}")
                    Transaccion.objects.create(
                        budget=budget,
                        tipo=tipo,
                        monto=monto,
                        descripcion=descripcion_trans,
                        pedido=pedido
                    )
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
        'form': form,
        'search_term': search_term
    })

@login_required
def buscar_productos(request):
    if request.user.rol not in ['Encargado de inventario', 'Empleado de ventas']:
        return JsonResponse([], safe=False)
    term = request.GET.get('term', '')
    productos = Producto.objects.filter(nombre__icontains=term)[:10]
    results = [{'id': p.id_producto, 'text': p.nombre} for p in productos]
    print(f"Productos encontrados: {results}")  # Depuración
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
    
    logger.info(f"Pedidos recuperados: {list(pedidos)}")

    pedidos_con_precio = []
    for pedido in pedidos:
        transaccion = Transaccion.objects.filter(pedido=pedido).first()
        if transaccion:
            total_precio = transaccion.monto
            logger.info(f"Pedido {pedido.id_pedido} usando transaccion.monto: {total_precio}")
        else:
            total_precio = sum(
                detalle.producto.precio * detalle.cantidad 
                for detalle in pedido.detallepedido_set.all()
            )
            logger.info(f"Pedido {pedido.id_pedido} calculado sin transacción: {total_precio}")
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