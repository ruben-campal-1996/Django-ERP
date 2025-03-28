# Generated by Django 5.1.7 on 2025-03-19 12:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Inventario", "0006_pedido_descripcion"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="cliente",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"rol": "Cliente"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
