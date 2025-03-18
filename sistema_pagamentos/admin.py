from django.contrib import admin
from sistema_pagamentos.models import Cliente

# Registrando modelos no nosso admin para criar clientes, tabela de preços, estoque, etc.


class Clientes(admin.ModelAdmin):
    list_display = ('id_cliente','nome_cliente','email_cliente','CNPJ') # Campos que queremos exibir no display do admin.
    list_display_links = ('id_cliente', 'nome_cliente') # Permite alterar o cliente clicando no ID ou nome.
    search_fields = ('nome_cliente','CNPJ',) # Permite buscar clientes pelo nome ou CNPJ.
    list_per_page = 20 # Paginação da quantidade de clientes que serao exibidos.

# Registrando configurações: 
# param(1) -> modelo que foi importado 
# param(2) -> configuração do modelo, ou seja, classe criada
admin.site.register(Cliente, Clientes)
