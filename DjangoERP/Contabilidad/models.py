from django.db import models

class Budget(models.Model):
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)  # Nuevo campo

    def __str__(self):
        return f"Budget actualizado el {self.fecha_actualizacion}"

    @property
    def monto(self):
        ingresos = self.transaccion_set.filter(tipo='ingreso').aggregate(total=models.Sum('monto'))['total'] or 0
        egresos = self.transaccion_set.filter(tipo='egreso').aggregate(total=models.Sum('monto'))['total'] or 0
        return self.monto_inicial + ingresos - egresos  # Incluye monto_inicial

class Transaccion(models.Model):
    TIPO_CHOICES = (
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    )
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    pedido = models.ForeignKey('Inventario.Pedido', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - ${self.monto} - {self.fecha}"