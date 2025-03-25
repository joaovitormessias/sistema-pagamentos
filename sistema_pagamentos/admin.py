from django.contrib import admin
from sistema_pagamentos.models import Cliente, Produto, Estoque, Pedido, Pagamento,  Venda

# Registrando modelos no nosso admin para criar clientes, tabela de preços, estoque, etc.


class Clientes(admin.ModelAdmin):
    list_display = ('id_cliente','nome_cliente','email_cliente','cnpj') # Campos que queremos exibir no display do admin.
    list_display_links = ('id_cliente', 'nome_cliente') # Permite alterar o cliente clicando no ID ou nome.
    search_fields = ('nome_cliente','cnpj',) # Permite buscar clientes pelo nome ou CNPJ.
    list_per_page = 20 # Paginação da quantidade de clientes que serao exibidos.

# Registrando configurações: 
# param(1) -> modelo que foi importado 
# param(2) -> configuração do modelo, ou seja, classe criada
admin.site.register(Cliente, Clientes)

class Produtos(admin.ModelAdmin):
    list_display = ('id_produto', 'nome_produto','preco_padrao','descricao_produto','data_validade_produto') # remover preco_padrao
    list_display_links = ('id_produto', 'nome_produto','preco_padrao')
    search_fields = ('id_produto','nome_produto',)
    list_per_page = 20

admin.site.register(Produto, Produtos)

class Estoques(admin.ModelAdmin):
    list_display = ('id_estoque', 'produto', 'quantidade_disponivel','valor_unitario', 'data_entrada', 'data_saida') # colocar preco_padrao
    list_display_links = ('id_estoque','produto')
    search_fields = ('id_estoque','produto',)
    list_per_page = 20

admin.site.register(Estoque,Estoques)

class Pedidos(admin.ModelAdmin):
    list_display = ('id_pedido','produto','quantidade_pedido', 'cliente', 'data_pedido')
    list_display_links = ('id_pedido','cliente')
    search_fields = ('id_pedido','cliente',)
    list_per_page = 20

admin.site.register(Pedido,Pedidos)

class Pagamentos(admin.ModelAdmin):
    list_display = ('id_pagamento', 'pedido', 'metodo_pagamento','quantidade_parcelas','data_pagamento', 'total_pedido','produtos_pedidos')
    list_display_links = ('id_pagamento','pedido')
    search_fields = ('id_pagamento',)
    list_per_page = 20

admin.site.register(Pagamento, Pagamentos)

class Vendas(admin.ModelAdmin):
    list_display = ('id_venda','pedido', 'cliente', 'pagamento','data_venda')
    list_display_links = ('id_venda','pedido', 'cliente')
    search_fields = ('id_venda',)
    list_per_page = 20
    
admin.site.register(Venda,Vendas)




