# Generated by Django 5.1.7 on 2025-03-19 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_pagamentos', '0013_remove_historicocompra_produto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicocompra',
            name='cliente',
        ),
    ]
