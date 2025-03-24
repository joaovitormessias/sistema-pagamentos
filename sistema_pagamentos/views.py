# Usando o pacote http para renderizar um JSON quando chegar uma requisicao para determinada URL.
from sistema_pagamentos.models import Cliente, Produto, Estoque, Pedido,  Venda, Pagamento
from rest_framework import viewsets, generics
from sistema_pagamentos.serializer import ClienteSerializer, ProdutoSerializer, EstoqueSerializer, PedidoSerializer,PagamentoSerializer,  VendaSerializer, ListaPedidosClienteSerializer

# Views. Utilizando dados da nossa base

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProdutosViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class EstoquesViewSet(viewsets.ModelViewSet):
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer

class PedidosViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PagamentosViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

class VendasViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

class ListaPedidosCliente(generics.ListAPIView):
    """Listando os pedidos de um Cliente"""
    def get_queryset(self):
        queryset = Pedido.objects.filter(cliente_id = self.kwargs['pk'])
        return queryset
    serializer_class = ListaPedidosClienteSerializer

