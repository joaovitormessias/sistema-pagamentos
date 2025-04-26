from celery import shared_task
from sistema_pagamentos.models import Produto, Pedido
from django.core.mail import send_mail
from decouple import config


@shared_task
def enviar_email(produto_id):

    '''
    Task assíncrona que envia um e-mail para os clientes informando sobre a alteração de preço de um produto.

    Parâmetros:
    - produto_id (int): ID do produto que teve seu preço alterado.

    A função verifica todos os pedidos que incluem o produto alterado e envia um e-mail aos respectivos clientes.
    '''

    produto = Produto.objects.get(id_produto=produto_id)

    pedidos = produto.itens_pedido.all() # Obtendo todos os itens de pedido do produto

    for item in pedidos:
        cliente = item.pedido.cliente # Obtendo o cliente associado ao pedido
        if cliente.user.email:
            mensagem = f'O preço do produto {produto.nome_produto} foi alterado para {produto.preco_unitario}. Verifique seus pedidos.'
            send_mail(
                'Alteração de Preço do Produto',
                mensagem,
                 config('EMAIL_HOST_USER'),
                [cliente.user.email],
                fail_silently=False,
                auth_user= config('EMAIL_HOST_USER'),   # E-mail de autenticação
                auth_password=config('EMAIL_HOST_PASSWORD'), # Senha de autenticação
            )