# Generated by Django 5.1.7 on 2025-03-18 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_pagamentos', '0007_alter_pagamento_data_pagamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='data_pagamento',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
