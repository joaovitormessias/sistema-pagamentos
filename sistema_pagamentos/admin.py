from django.contrib import admin
from sistema_pagamentos.models import Cliente, Produto, Pedido, Pagamento, ItensPedido

# Register your models here.
class Clientes(admin.ModelAdmin):
    list_display = ('nome_cliente', 'cnpj', 'user')
    list_display_links = ( 'nome_cliente',)
    search_fields = ('nome_cliente', 'cnpj',)
    list_per_page = 20

admin.site.register(Cliente, Clientes)

class Produtos(admin.ModelAdmin):
    list_display = ('id_produto', 'nome_produto','descricao')
    list_display_links = ('id_produto','nome_produto')
    search_fields = ('id_produto', 'nome_produto',)
    list_per_page = 20

admin.site.register(Produto, Produtos)

class ItensInline(admin.TabularInline):
    model = ItensPedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = (ItensInline,)
    list_display = ('id_pedido', 'cliente')
    list_display_links = ('id_pedido','cliente')
    search_fields = ('id_pedido','cliente',)
    list_per_page = 20


class Pagamentos(admin.ModelAdmin):
    list_display = ('id_pagamento', 'status_pagamento','data_pagamento')
    list_display_links = ('id_pagamento',)
    search_fields = ('id_pagamento',)
    list_per_page = 20

admin.site.register(Pagamento, Pagamentos)
