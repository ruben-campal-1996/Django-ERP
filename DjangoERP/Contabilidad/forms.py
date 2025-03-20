from django import forms
from .models import Budget, Movimiento

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['presupuesto_total', 'entradas', 'salidas']

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['tipo', 'monto', 'descripcion']