# Generated by Django 5.1.7 on 2025-03-18 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_pagamentos', '0006_pedido_quantidade_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='data_pagamento',
            field=models.DateTimeField(null=True),
        ),
    ]
