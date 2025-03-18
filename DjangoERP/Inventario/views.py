from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Producto, MovimientoStock
from .forms import ProductoForm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

@login_required
def inventario_view(request):
    if request.user.rol != 'Encargado de inventario':
        return redirect('usuarios:logistics')
    productos = Producto.objects.all()
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
            for prod_id in productos_ids:
                try:
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
                    else:
                        messages.error(request, f"Stock insuficiente para {producto.nombre}")
                        return redirect('inventario:inventario')
                except Producto.DoesNotExist:
                    messages.error(request, "Producto no encontrado.")
                    return redirect('inventario:inventario')
            messages.success(request, 'Pedido registrado exitosamente.')
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

    # Obtener todos los movimientos
    movimientos = MovimientoStock.objects.all().order_by('-fecha')

    # Crear buffer para el PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Registro de Movimientos de Inventario", styles['Heading1']))

    # Datos para la tabla
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

    # Crear la tabla
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

    # Generar el PDF
    doc.build(elements)
    buffer.seek(0)

    # Respuesta HTTP con el PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="registro_movimientos.pdf"'
    return response

@login_required
def descargar_inventario(request):
    if request.user.rol != 'Encargado de inventario':
        return redirect('usuarios:logistics')

    # Obtener todos los productos
    productos = Producto.objects.all().order_by('id_producto')

    # Crear buffer para el PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    # Crear un estilo personalizado con alineación centrada
    centered_style = styles['Heading1']
    centered_style.alignment = 1  # 0=izquierda, 1=centro, 2=derecha
    elements.append(Paragraph("Registro de Inventario", centered_style))

    # Datos para la tabla (sin Descripción)
    data = [['ID', 'Nombre', 'Precio', 'Stock']]
    for prod in productos:
        data.append([
            prod.id_producto,
            prod.nombre,
            f"${prod.precio}",
            prod.stock
        ])

    # Crear la tabla
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

    # Generar el PDF
    doc.build(elements)
    buffer.seek(0)

    # Respuesta HTTP con el PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="registro_inventario.pdf"'
    return response