from django.db import models
import random

class Producto(models.Model):
    id_producto = models.CharField(max_length=5, primary_key=True, unique=True)
    nombre = models.CharField(max_length=200)  # VARCHAR(200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Número con 2 decimales
    stock = models.PositiveIntegerField()  # Número entero positivo
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Campo opcional para imágenes

    def save(self, *args, **kwargs):
        # Generamos un ID aleatorio de 5 cifras si no existe
        if not self.id_producto:
            while True:
                new_id = str(random.randint(10000, 99999))
                if not Producto.objects.filter(id_producto=new_id).exists():
                    self.id_producto = new_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
