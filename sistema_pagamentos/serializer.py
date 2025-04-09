from rest_framework import serializers
from sistema_pagamentos.models import Cliente, Produto, Pedido, Pagamento, ItensPedido

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class ItensPedidoSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    produto = ProdutoSerializer(read_only=True)
    class Meta:
        model = ItensPedido
        fields = ('produto', 'quantidade','total')

    def get_total(self, instance):
        return instance.quantidade * instance.produto.preco_unitario

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItensPedidoSerializer(many=True)
    cliente = ClienteSerializer()
    
    class Meta:
        model = Pedido
        fields = ('id_pedido','cliente', 'itens','total')
        depth = 1

class CriarEditarItensPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItensPedido
        fields = ('produto', 'quantidade')

class CriarEditarPedidoSerializer(serializers.ModelSerializer):
    itens = CriarEditarItensPedidoSerializer(many=True)
    class Meta:
        model = Pedido
        fields = ('cliente','itens')      

    def create(self, validated_data):
        itens = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item in itens:
            ItensPedido.objects.create(pedido= pedido, **item)
        pedido.save()
        return pedido
    
    def update(self, instance, validated_data):
        itens = validated_data.pop('itens')
        if itens:
            instance.itens.all()
            for item in itens:
                ItensPedido.objects.create(pedido = instance, **item)
            instance.save()
        return instance
    pass


class PagamentoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    pedido = PedidoSerializer(read_only=True)

    class Meta:
        model = Pagamento
        fields = '__all__'
        depth = 1
