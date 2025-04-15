from rest_framework import serializers
from sistema_pagamentos.models import Cliente, Produto, Pedido, Pagamento, ItensPedido

# Aqui serializamos os dados, ou seja, transformamos os dados dentro  
# do nosso banco de dados para que a aplicação web veja as informações em JSON nas views


class ClienteSerializer(serializers.ModelSerializer):
    '''Exibe todos os dados relacionados ao mmeu cliente'''
    class Meta:

        # model: tabela que contém as informações que serão serializadas
        # fields: campos que eu quero serializar da minha tabela

        model = Cliente
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    '''Exibe todas as informações do produto para a aplicacao'''
    class Meta:
        model = Produto
        fields = '__all__'

class ItensPedidoSerializer(serializers.ModelSerializer):
    '''Exibe todos os itens do pedido do cliente'''
    total = serializers.SerializerMethodField() # instancia do calculo 'TOTAL' 
    produto = ProdutoSerializer(read_only=True) # exibe a informação completa do produto
    class Meta:
        model = ItensPedido
        fields = ('produto', 'quantidade','total')

    # Função que retorna o total de cada item pedido
    def get_total(self, instance):
        return instance.quantidade * instance.produto.preco_unitario

class PedidoSerializer(serializers.ModelSerializer):
    '''Exibe todas informações do pedido do cliente incluindo os itens dentro do pedido'''
    itens = ItensPedidoSerializer(many=True) # exibe todos os itens dentro do pedido
    cliente = ClienteSerializer()
    
    class Meta:
        model = Pedido
        fields = ('id_pedido','cliente', 'itens','total')
        depth = 1

class CriarEditarItensPedidoSerializer(serializers.ModelSerializer):
    '''Permite com que outra aplicação consiga realizar o crud dos meus itens'''
    class Meta:
        model = ItensPedido
        fields = ('produto', 'quantidade')

class CriarEditarPedidoSerializer(serializers.ModelSerializer):
    '''Permite com que outra aplicação consiga realizar o crud dos meus pedidos'''
    itens = CriarEditarItensPedidoSerializer(many=True)
    class Meta:
        model = Pedido
        fields = ('cliente','itens')      

    def create(self, validated_data):
        '''Verifica se o pedido do item ja existe, se nao existir ele cria'''
        itens = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item in itens:
            ItensPedido.objects.create(pedido= pedido, **item)
        pedido.save()
        return pedido
    
    def update(self, instance, validated_data):
        '''Atualiza a informacao de determinado pedido de item'''
        itens = validated_data.pop('itens')
        if itens:
            instance.itens.all()
            for item in itens:
                ItensPedido.objects.create(pedido = instance, **item)
            instance.save()
        return instance
    pass


class PagamentoSerializer(serializers.ModelSerializer):
    '''Exibe as informações do pagamento realizado pelo cliente'''

    cliente = ClienteSerializer(read_only=True) # exibe informações do cliente completa
    pedido = PedidoSerializer(read_only=True) # exibe informações completa do pedido

    class Meta:
        model = Pagamento
        fields = '__all__'
        depth = 1 # exibe mais detalhes do meu pagamento
