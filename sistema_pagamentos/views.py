# Modelos da nossa base de dados: é de onde a API vai extrair as informações exigidas
from sistema_pagamentos.models import Cliente, Produto, Pedido, Pagamento

# Biblioteca do Django Rest que permite criar as viewsets 
from rest_framework import viewsets

# Serializadores: serão responsáveis por transformar esses dados da nossa base de dados para o formato JSON
from sistema_pagamentos.serializer import ClienteSerializer, ProdutoSerializer, PedidoSerializer, PagamentoSerializer, CriarEditarPedidoSerializer

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse

# --------------------------------- VIEWS DO DJANGO --------------------------------- #

class ClientesViewSet(viewsets.ModelViewSet):

    '''
    ViewSet para gerenciar os dados de clientes no sistema.
    '''

    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProdutosViewSet(viewsets.ModelViewSet):

    '''
    ViewSet para gerenciar os dados de produtos no sistema.
    '''

    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class PedidosViewSet(viewsets.ModelViewSet):

    '''
    ViewSet para gerenciar os pedidos no sistema.
    
    Define o serializer a ser usado dependendo da ação (list/retrieve ou create/update).
    '''
    
    queryset = Pedido.objects.all()
    

    def get_serializer_class(self):  
        '''Essa função permite o usuário fazer uma alteração do pedido'''           
        if self.action == 'list' or self.action == 'retrieve':
            return PedidoSerializer
        return CriarEditarPedidoSerializer

class PagamentosViewSet(viewsets.ModelViewSet):

    '''
    ViewSet para gerenciar os pagamentos no sistema.
    '''

    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer


def gerar_relatorio_pedidos(request, cliente_id):

    '''
    Gera um relatório de pedidos realizados por um cliente específico.
    
    Parâmetros:
    - cliente_id (int): ID do cliente para o qual o relatório será gerado.
    
    Retorna:
    - Um arquivo PDF com os detalhes dos pedidos do cliente.
    '''

    pedidos = Pedido.objects.filter(cliente_id=cliente_id) # Filtra os pedidos do cliente especificado

    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter) # Cria um buffer para o PDF

    p.setFont("Helvetica", 12)
    p.drawString(100, 50, f"Relatório de Pedidos - Cliente {cliente_id}")

    y_position = 750

    for pedido in pedidos:
        p.drawString(100, y_position, f"Pedido ID: {pedido.id_pedido}")
        y_position -= 20  
        p.drawString(100, y_position, f"Total: {pedido.total}")
        y_position -= 20  
        p.drawString(100, y_position, f"Cliente: {pedido.cliente.nome_cliente}")
        y_position -= 40  

        for item in pedido.itens.all():
            p.drawString(100, y_position, f"Produto: {item.produto.nome_produto}")
            p.drawString(300, y_position, f"Quantidade: {item.quantidade}")
            p.drawString(400, y_position, f"Preço Unitário: {item.produto.preco_unitario}")
            y_position -= 20
        p.drawString(90, y_position, f"Total Pedido: {pedido.total}")
        y_position -= 40

    p.showPage() # Finaliza a página
    p.save() # Salva o PDF no buffer

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf') # Retorna o PDF como resposta HTTP

