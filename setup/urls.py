# URLs.

from django.contrib import admin
from django.urls import path
from sistema_pagamentos.views import clientes # View de clientes.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', clientes), # Visualizar o JSON dentro da view clientes
]
