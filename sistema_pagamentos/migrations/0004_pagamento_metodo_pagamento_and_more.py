# Generated by Django 5.1.7 on 2025-03-18 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema_pagamentos', '0003_remove_pagamento_metodo_pagamento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='metodo_pagamento',
            field=models.CharField(choices=[('cartao', 'Cartão'), ('boleto', 'Boleto'), ('pix', 'PIX'), ('dinheiro', 'Dinheiro'), ('transferencia', 'Transferência')], default='cartao', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pagamento',
            name='quantidade_parcelas',
            field=models.CharField(choices=[('avista', 'Avista'), ('duas', '2x'), ('tres', '3x'), ('quatro', '4x'), ('cinco', '5x'), ('seis', '6x'), ('sete', '7x'), ('oito', '8x'), ('nove', '9x'), ('dez', '10x'), ('onze', '11x'), ('doze', '12x')], default='avista', max_length=10, null=True),
        ),
    ]
