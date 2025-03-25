from rest_framework import serializers
from sistema_pagamentos.models import Cliente, Produto, Estoque, Pedido,  Venda, Pagamento

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id_cliente','nome_cliente','email_cliente','cnpj']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id_produto','nome_produto','preco_padrao', 'descricao_produto', 'data_validade_produto'] # remover preco_padrao

class EstoqueSerializer(serializers.ModelSerializer):
    produto = serializers.ReadOnlyField(source='produto.nome_produto')
    class Meta:
        model = Estoque
        fields = ['id_estoque','produto','quantidade_disponivel', 'valor_unitario', 'data_entrada', 'data_saida'] # adicionar preco_padrao

class PedidoSerializer(serializers.ModelSerializer):
    cliente = serializers.ReadOnlyField(source='cliente.nome_cliente')
    produto = serializers.ReadOnlyField(source='produto.nome_produto')
    class Meta:
        model = Pedido
        fields = ['id_pedido','cliente','produto','quantidade_pedido','data_pedido','status_pedido']

class PagamentoSerializer(serializers.ModelSerializer):
    pedido = serializers.ReadOnlyField(source='pedido.produto.nome_produto')
    class Meta:
        model = Pagamento
        fields = ['id_pagamento','pedido','metodo_pagamento','quantidade_parcelas','status_pagamento','data_pagamento', 'total_pedido', 'produtos_pedidos']

class VendaSerializer(serializers.ModelSerializer):
    pedido = serializers.ReadOnlyField(source='pagamento.pedido.produto.nome_produto')
    cliente = serializers.ReadOnlyField(source='pagamento.pedido.cliente.nome_cliente')
    pagamento = serializers.ReadOnlyField(source='pagamento.metodo_pagamento')
    class Meta:
        model = Venda
        fields = ['id_venda','pedido','cliente','pagamento','data_venda','status_venda']

# listanto os pedidos feitos pelo cliente
class ListaPedidosClienteSerializer(serializers.ModelSerializer):
    produto = serializers.ReadOnlyField(source='produto.nome_produto')
    class Meta:
        model = Pedido
        fields = ['produto','quantidade_pedido','data_pedido']


