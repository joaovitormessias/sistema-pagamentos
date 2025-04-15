# Biblioteca do Django que permite a criação do admin do django, facilitando a visualização das nossas entidades.
from django.contrib import admin

# Modelo das entidades da nossa base de dados.
from sistema_pagamentos.models import Cliente, Produto, Pedido, Pagamento, ItensPedido 

# Nesse arquivo nós exibimos as informações contidas dentro do meu banco de dados no admin do Django.
# Permitindo: visualizar, criar, editar ou deletar dados.
# É uma interface que permite interação direta com o banco de dados.

class Clientes(admin.ModelAdmin):
    '''Exibe informções dos clientes na minha base de dados'''

     # list_display: colunas que serâo exibidas no meu django admin
     # list_display_links: link de acesso ao objeto
     # search_fields: campo de busca
     # list_per_page: paginação, permite eu vizualizar 20 itens por página

    list_display = ('nome_cliente', 'cnpj', 'user')
    list_display_links = ( 'nome_cliente',) 
    search_fields = ('nome_cliente', 'cnpj',) 
    list_per_page = 20 

# Registra a minha entidade Cliente dentro do admin
admin.site.register(Cliente, Clientes)

class Produtos(admin.ModelAdmin):
    '''Exibe informações dos produtos contido na minha base de dados'''

    list_display = ('id_produto', 'nome_produto','descricao')
    list_display_links = ('id_produto','nome_produto')
    search_fields = ('id_produto', 'nome_produto',)
    list_per_page = 20

# Registra minha entidade Proodutos no meu admin
admin.site.register(Produto, Produtos)

class ItensInline(admin.TabularInline):
    '''Exibe os itens dentro do pedido realizado pelo cliente'''

    model = ItensPedido

# Registra a informação dentro do meu pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    '''Exibe os pedidos realizados pelo meu cliente, isso inclui os itens dentro de cada pedido'''

    inlines = (ItensInline,)
    list_display = ('id_pedido', 'cliente')
    list_display_links = ('id_pedido','cliente')
    search_fields = ('id_pedido','cliente',)
    list_per_page = 20


class Pagamentos(admin.ModelAdmin):
    '''Exibe os pagamentos realizados dos clientes'''
    
    list_display = ('id_pagamento', 'status_pagamento','data_pagamento')
    list_display_links = ('id_pagamento',)
    search_fields = ('id_pagamento',)
    list_per_page = 20

# Registra as informações da minha entidade do Pagamento no meu admin
admin.site.register(Pagamento, Pagamentos)
