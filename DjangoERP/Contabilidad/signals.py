'''from django.db.models.signals import post_save
from django.dispatch import receiver
from Inventario.models import Pedido
from .models import Budget, Transaccion

@receiver(post_save, sender=Pedido)
def crear_transaccion_al_guardar_pedido(sender, instance, created, **kwargs):
    print(f"Signal disparado para pedido {instance.id_pedido}, creado: {created}")
    if created:
        print(f"Procesando pedido {instance.id_pedido} del cliente {instance.cliente}")
        if Transaccion.objects.filter(pedido=instance).exists():
            print(f"Transacción ya existe para {instance.id_pedido}")
            return

        detalles = instance.detallepedido_set.all()
        print(f"Detalles encontrados: {list(detalles)}")
        monto = sum(
            detalle.producto.precio * detalle.cantidad
            for detalle in detalles
        )
        print(f"Monto calculado: {monto}")
        
        budget = Budget.objects.first()
        if not budget:
            budget = Budget.objects.create()
            print("Budget creado")

        rol = instance.cliente.rol
        print(f"Rol del cliente: {rol}")
        if rol == 'Encargado de inventario':
            tipo = 'egreso'
            descripcion = f"Gasto por pedido {instance.id_pedido} (reabastecimiento)"
        elif rol in ['Cliente', 'Empleado de ventas']:
            tipo = 'ingreso'
            descripcion = f"Ingreso por pedido {instance.id_pedido} (venta)"
        else:
            print(f"Rol no reconocido: {rol}")
            return

        print(f"Creando transacción: {tipo} - ${monto} - {descripcion}")
        Transaccion.objects.create(
            budget=budget,
            tipo=tipo,
            monto=monto,
            descripcion=descripcion,
            pedido=instance
        )
        print(f"Transacción creada para {instance.id_pedido}")'''