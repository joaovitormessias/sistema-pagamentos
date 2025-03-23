# URLs.

from django.contrib import admin
from django.urls import path, include
from sistema_pagamentos.views import ClientesViewSet, ProdutosViewSet, EstoquesViewSet, PedidosViewSet, TabelaPrecosViewSet, PagamentosViewSet, VendasViewSet, HistoricoComprasViewSet
from rest_framework import routers


# Rota padrão(principal) dada pelo django rest
router = routers.DefaultRouter()

# Registrando rotas
router.register('clientes', ClientesViewSet, basename='Clientes')
router.register('produtos', ProdutosViewSet, basename='Produtos')
router.register('estoques', EstoquesViewSet, basename='Estoques')
router.register('pedidos', PedidosViewSet, basename='Pedidos')
router.register('tabelaprecos', TabelaPrecosViewSet, basename='TabelaPrecos')
router.register('pagamentos', PagamentosViewSet, basename='Pagamentos')
router.register('vendas', VendasViewSet, basename='Vendas')
router.register('historicocompras', HistoricoComprasViewSet, basename='HistoricoCompras')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
]
