
from django.contrib import admin
from django.urls import path, include
from sistema_pagamentos.views import ClientesViewSet, ProdutosViewSet, PedidosViewSet, PagamentosViewSet

# Autenticação
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import routers

# Documentação
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


# Endpoints
router = routers.DefaultRouter()

router.register('clientes', ClientesViewSet, basename='Clientes')
router.register('produtos', ProdutosViewSet, basename='Produtos')
router.register('pedidos', PedidosViewSet, basename='Pedidos')
router.register('pagamentos', PagamentosViewSet, basename='Pagamentos')

urlpatterns = [

    # Rota do admin
    path('admin/', admin.site.urls),

    # Documentação 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), 
    # UI (USER INTERFACE) opicional:
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), 

    # Autenticação
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

    # Registrando os endpoints
    path('api/',include(router.urls)), 

]
