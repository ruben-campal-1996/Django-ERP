# Inventario/models.py
from django.db import models
from django.conf import settings
import random

class Producto(models.Model):
    id_producto = models.CharField(max_length=5, primary_key=True, unique=True)
    nombre = models.CharField(max_length=200)  # VARCHAR(200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Número con 2 decimales
    stock = models.PositiveIntegerField()  # Número entero positivo
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Campo opcional para imágenes

    def save(self, *args, **kwargs):
        if not self.id_producto:
            while True:
                new_id = str(random.randint(10000, 99999))
                if not Producto.objects.filter(id_producto=new_id).exists():
                    self.id_producto = new_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class MovimientoStock(models.Model):
    TIPO_MOVIMIENTO = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.tipo} de {self.cantidad} unidades de {self.producto.nombre} el {self.fecha}"