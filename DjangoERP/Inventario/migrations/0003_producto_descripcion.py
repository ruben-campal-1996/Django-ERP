# Generated by Django 5.1.7 on 2025-03-18 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Inventario", "0002_producto_imagen"),
    ]

    operations = [
        migrations.AddField(
            model_name="producto",
            name="descripcion",
            field=models.TextField(blank=True, null=True),
        ),
    ]
