# Generated by Django 5.1.7 on 2025-03-25 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "Contabilidad",
            "0002_remove_budget_created_at_remove_budget_entradas_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="budget",
            name="monto_inicial",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
