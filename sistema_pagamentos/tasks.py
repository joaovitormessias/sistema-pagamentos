"""Background notifications; broker/SMTP delivery is not exactly-once."""
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from sistema_pagamentos.models import Produto


@shared_task
def enviar_email(produto_id):
    """Send once per recipient per task, even when a buyer has several orders."""
    produto = Produto.objects.filter(pk=produto_id).first()
    if produto is None:
        return 0
    recipients = set(produto.itens_pedido.values_list('pedido__cliente__user__email', flat=True))
    sent = 0
    for email in sorted(recipients - {''}):
        sent += send_mail(
            'Alteração de Preço do Produto',
            f'O preço do produto {produto.nome_produto} foi alterado para {produto.preco_unitario}. Verifique seus pedidos.',
            settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False,
        )
    return sent
