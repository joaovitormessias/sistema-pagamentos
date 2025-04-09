from sistema_pagamentos.models import Cliente, Produto, Pedido, Pagamento
from rest_framework import viewsets
from sistema_pagamentos.serializer import ClienteSerializer, ProdutoSerializer, PedidoSerializer, PagamentoSerializer, CriarEditarPedidoSerializer

# Create your views here.

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProdutosViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class PedidosViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    # serializer_class = PedidoSerializer

    def get_serializer_class(self):             
        if self.action == 'list' or self.action == 'retrieve':
            return PedidoSerializer
        return CriarEditarPedidoSerializer

class PagamentosViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
