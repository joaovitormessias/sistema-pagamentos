# Usando o pacote http para renderizar um JSON quando chegar uma requisicao para determinada URL.
from django.http import JsonResponse
from sistema_pagamentos.models import Cliente, Produto, Estoque, Pedido, TabelaPreco,  Venda, HistoricoCompra, Pagamento
from rest_framework import viewsets
from sistema_pagamentos.serializer import ClienteSerializer, ProdutoSerializer, EstoqueSerializer, PedidoSerializer, TabelaPrecoSerializer,PagamentoSerializer,  VendaSerializer, HistoricoCompraSerializer

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

class TabelaPrecos(viewsets.ModelViewSet):
    queryset = TabelaPreco
    serializer_class = TabelaPrecoSerializer

class PagamentosViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer

class VendasViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

class HistoricoComprasViewSet(viewsets.ModelViewSet):
    queryset = HistoricoCompra.objects.all()
    serializer_class = HistoricoCompraSerializer