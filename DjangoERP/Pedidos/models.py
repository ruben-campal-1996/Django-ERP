from django.db import models
from django.utils import timezone
import random

class Pedido(models.Model):
    id_pedido = models.CharField(max_length=7, primary_key=True, unique=True)
    nombre = models.CharField(max_length=200)  # VARCHAR(200)
    fecha = models.DateTimeField(default=timezone.now)  # Fecha del pedido
    usuario = models.ForeignKey('Usuarios.Usuario', on_delete=models.CASCADE)  # Relación con Usuario
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Precio total

    def save(self, *args, **kwargs):
        # Generamos un ID aleatorio de 7 cifras si no existe
        if not self.id_pedido:
            while True:
                new_id = str(random.randint(1000000, 9999999))
                if not Pedido.objects.filter(id_pedido=new_id).exists():
                    self.id_pedido = new_id
                    break
        super().save(*args, **kwargs)

    def calcular_precio_final(self):
        # Calcula el precio total sumando los precios de los detalles
        total = sum(item.precio_total for item in self.detalles_pedido.all())
        self.precio_final = total
        self.save()
        return total

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles_pedido', on_delete=models.CASCADE)
    producto = models.ForeignKey('Inventario.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()  # Cantidad de productos
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto en el momento del pedido

    @property
    def precio_total(self):
        # Calcula el precio total del detalle (cantidad * precio unitario)
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        # Asigna el precio unitario del producto si no está definido
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido {self.pedido.id_pedido}"
