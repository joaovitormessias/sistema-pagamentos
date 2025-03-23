from rest_framework import serializers
from sistema_pagamentos.models import Cliente, Produto, Estoque, Pedido, TabelaPreco,  Venda, HistoricoCompra, Pagamento

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id_cliente','nome_cliente','email_cliente','CNPJ']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id_produto','nome_produto', 'preco_padrao', 'descricao_produto', 'data_validade_produto']

class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = ['id_estoque','produto','quantidade_disponivel', 'data_entrada', 'data_saida']

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id_pedido','cliente','produto','quantidade_pedido','data_pedido','status_pedido']

class TabelaPrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaPreco
        fields = ['id_tabela','cliente','produto','preco_personalizado']

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = ['id_pagamento','pedido','metodo_pagamento','quantidade_parcelas','status_pagamento','data_pagamento']


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = ['id_venda','pedido','cliente','pagamento','data_venda','status_venda']

class HistoricoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoCompra
        fields = ['id_historico','venda','exibir_cliente']