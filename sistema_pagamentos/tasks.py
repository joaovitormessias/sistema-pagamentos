from celery import shared_task
from sistema_pagamentos.models import Venda
from django.core.mail import send_mail

@shared_task
def notoficar_cliente(venda_id):
    venda = Venda.objects.get(id_venda=venda_id)
    produto = venda.pedido.produto

    message = f'O preço do produto {produto.nome_produto} que você comprou foi reduzido para {produto.preco_padrao}'

    send_mail(
        'Notificação de Redução de Preço',
        message,
        'joaovitormessias30@gmail.com',
        [venda.cliente.email_cliente],
        fail_silently=False,
    )