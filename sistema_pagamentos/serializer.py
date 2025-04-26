from rest_framework import serializers
from sistema_pagamentos.models import Cliente, Produto, Pedido, Pagamento, ItensPedido

# -------------------------------- SERIALIZANDO DADOS -------------------------------- #



class ClienteSerializer(serializers.ModelSerializer):

    '''
    Serializer para a entidade Cliente, transformando o modelo Cliente em um formato que pode ser facilmente
    convertido para JSON ou outro formato.
    '''

    class Meta:
        model = Cliente
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):

    '''
    Serializer para a entidade Produto, transformando o modelo Produto em um formato serializável.
    '''

    class Meta:
        model = Produto
        fields = '__all__'

class ItensPedidoSerializer(serializers.ModelSerializer):

    '''
    Serializer para a entidade ItensPedido, que inclui o cálculo do total do item (quantidade * preço).
    '''

    total = serializers.SerializerMethodField()
    produto = ProdutoSerializer(read_only=True)
    class Meta:
        model = ItensPedido
        fields = ('produto', 'quantidade','total')

    # Função que retorna o total de cada item pedido
    def get_total(self, instance):

        '''
        Método para calcular o valor total de um item baseado na quantidade e no preço unitário do produto.
        '''

        return instance.quantidade * instance.produto.preco_unitario

class PedidoSerializer(serializers.ModelSerializer):

    '''
    Serializer para a entidade Pedido, que inclui os itens do pedido e informações do cliente.
    '''

    itens = ItensPedidoSerializer(many=True)
    cliente = ClienteSerializer()
    
    class Meta:
        model = Pedido
        fields = ('id_pedido','cliente', 'itens','total')
        depth = 1

class CriarEditarItensPedidoSerializer(serializers.ModelSerializer):

    '''
    Serializer para criação e edição dos itens de um pedido.
    '''

    class Meta:
        model = ItensPedido
        fields = ('produto', 'quantidade')

class CriarEditarPedidoSerializer(serializers.ModelSerializer):

    '''
    Serializer para criação e edição de um pedido, incluindo seus itens.
    '''

    itens = CriarEditarItensPedidoSerializer(many=True)
    class Meta:
        model = Pedido
        fields = ('cliente','itens')      

    def create(self, validated_data):

        '''
        Criação de um pedido novo, incluindo seus itens.
        '''

        itens = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item in itens:
            ItensPedido.objects.create(pedido= pedido, **item)
        pedido.save()
        return pedido
    
    def update(self, instance, validated_data):

        '''
        Atualização de um pedido existente, incluindo a atualização de seus itens.
        '''

        itens = validated_data.pop('itens')
        if itens:
            instance.itens.all()
            for item in itens:
                ItensPedido.objects.create(pedido = instance, **item)
            instance.save()
        return instance
    pass


class PagamentoSerializer(serializers.ModelSerializer):

    '''
    Serializer para a entidade Pagamento, incluindo informações do cliente e do pedido.
    '''
    
    cliente = ClienteSerializer(read_only=True)
    pedido = PedidoSerializer(read_only=True)

    class Meta:
        model = Pagamento
        fields = '__all__'
        depth = 1 # exibe mais detalhes do meu pagamento
