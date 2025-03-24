# URLs.

from django.contrib import admin
from django.urls import path, include
from sistema_pagamentos.views import ClientesViewSet, ProdutosViewSet, EstoquesViewSet, PedidosViewSet, PagamentosViewSet, VendasViewSet, ListaPedidosCliente
from rest_framework import routers


# Rota padrão(principal) dada pelo django rest
router = routers.DefaultRouter()

# Registrando rotas
router.register('clientes', ClientesViewSet, basename='Clientes')
router.register('produtos', ProdutosViewSet, basename='Produtos')
router.register('estoques', EstoquesViewSet, basename='Estoques')
router.register('pedidos', PedidosViewSet, basename='Pedidos')
router.register('pagamentos', PagamentosViewSet, basename='Pagamentos')
router.register('vendas', VendasViewSet, basename='Vendas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('cliente/<int:pk>/pedidos/', ListaPedidosCliente.as_view()),
]
