# Modelos da nossa base de dados: é de onde a API vai extrair as informações exigidas
from sistema_pagamentos.models import Cliente, Produto, Pedido, Pagamento

# Biblioteca do Django Rest que permite criar as viewsets 
from rest_framework import viewsets

# Serializadores: serão responsáveis por transformar esses dados da nossa base de dados para o formato JSON
from sistema_pagamentos.serializer import ClienteSerializer, ProdutoSerializer, PedidoSerializer, PagamentoSerializer, CriarEditarPedidoSerializer

# Aqui é como vamos exibir essas informações para a aplicação

class ClientesViewSet(viewsets.ModelViewSet):
    '''
    Exibe as informações do cliente, ele faz uma queryset e serializa esses dados transformando elas em um formato JSON.
    '''

    # queryset: vai pegar todos os objetos que a aquela entidade possui.
    # serializer_class: vai usar a função que criamos do serializer para transformar esses dados.
    
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProdutosViewSet(viewsets.ModelViewSet):
    '''
    Exibe as informações dos produtos onde ele faz uma quary que busca os dados referentes ao produto
    em seguida ele serializa essas informações para transformar elas em dados do tipo JSON. 
    '''
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class PedidosViewSet(viewsets.ModelViewSet):
    '''
    Exibe as informações referentes ao pedido feito pelo cliente que esta armazenado no banco de dados.
        A função get_serializer permite eu realizar a ação de poder criar ou editar um pedido.
        Por fim ela transforma essa minha informação em JSON.
    '''
    queryset = Pedido.objects.all()
    # serializer_class = PedidoSerializer

    def get_serializer_class(self):  
        '''Essa função permite o usuário fazer uma alteração do pedido'''           
        if self.action == 'list' or self.action == 'retrieve':
            return PedidoSerializer
        return CriarEditarPedidoSerializer

class PagamentosViewSet(viewsets.ModelViewSet):
    '''
    Exibe as informações dos pagamentos realizados pelos clientes, onde ele realiza a query dos dados solicitados.
        A partir disso ele serializa esses dados transformando em um formato JSON.
    '''
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
