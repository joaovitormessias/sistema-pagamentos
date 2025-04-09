from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_cliente = models.CharField(max_length=100, blank=False)
    cnpj = models.CharField(max_length=14, blank=True)

    def __str__(self):
        return self.nome_cliente

class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=100, blank=False)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    descricao = models.TextField()
    
    def __str__(self):
        return self.nome_produto
    

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    # cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')

    def __str__(self):
        return self.cliente.nome_cliente
    
    @property
    def total(self):
        queryset= self.itens.all().aggregate(
            total=models.Sum(models.F('quantidade') * models.F('produto__preco_unitario'))
        )

        return queryset['total']
                                   

class ItensPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='+') # o pedido pode ser apagado mas o produto nao
    quantidade = models.IntegerField()
    


class Pagamento(models.Model):
    id_pagamento = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    status_pagamento = models.CharField(
        max_length=20,
        choices= [('naorealizado','Não realizado'),('realizado','Realizado'),('emandamento','Em andamento'),('recusado','Recusado')],
        default= 'naorealizado'
    )
    data_pagamento = models.DateTimeField(auto_now_add=True)




    

    
