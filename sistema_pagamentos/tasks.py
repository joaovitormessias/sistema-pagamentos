from celery import shared_task
from django.core.mail import send_mail
from sistema_pagamentos.models import Pagamento

@shared_task
def notoficar_cliente(id_pagamento):
    try:
        pagamento = Pagamento.objects.get(id_pagamento=id_pagamento)
    except Pagamento.DoesNotExist:
        print(f'Pagamento com ID {id_pagamento} não encontrada') #log de erro
    
    produto = pagamento.pedido.produto

    message = f'O preço do produto {produto.nome_produto} que você comprou foi reduzido para {produto.preco_padrao}'

    send_mail(
        'Notificação de Redução de Preço',
        message,
        'email-457@jovial-world-422618-a5.iam.gserviceaccount.com',
        [pagamento.pedido.cliente.email_cliente],
        fail_silently=False,
    )