from django.db import models
from django.contrib.auth.models import User


# Criamos nossas entidades de acordo com as 
# É a partir daqui que nossa API vai consultar os dados de acordo com a pedido do cliente
class Cliente(models.Model):
    '''
    Modelo de entidade do Cliente

    params: id_cliente (pk): chave primária 
    params: user (onetoone): representação do usuario cadastrado dentro do django admin
    params: nome_cliente (char): nome do cliente
    params: cnpj (char): identificador unico da empresa

    '''

    id_cliente = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # CASCADE 'se eu apagar o cliente tudo relacionado ao usuario sera apagado
    nome_cliente = models.CharField(max_length=100, blank=False)
    cnpj = models.CharField(max_length=14, blank=True)

    def __str__(self):
        return self.nome_cliente

class Produto(models.Model):

    '''
    Representa o produto que sera usado dentro do meu pedido realizado pelo meu clinte e aparecera dentro dos pagamentos

    params: id_produto (pk): chave primeria da minha entidade Produto
    params: nome_produto (char): representa o nome que aquele produto tera dentro da base de dados
    params: preco_unitario (decimal): representa o valor que aquele produto tera dentro da base de dados 
    params: quantidade (int): esse atributo é responsável por determinar quantos produtos eu tenho na base de dados
    params: descricao (text): uma breve descricao do que se trata o produto  

    '''
    id_produto = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=100, blank=False)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    descricao = models.TextField()
    
    def __str__(self):
        return self.nome_produto
    

class Pedido(models.Model):

    '''
    
    A entidade Pedido representa o relacionamento entre o meu cliente e o produto

    params: id_pedido (pk): chave primaria, representa o id do pedido realizado pelo cliente
    params: cliente (fk): chave estrangeira que herda os atributos da minha entidade Cliente e possui uma relacao com os pedidos

    '''
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    # cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')

    def __str__(self):
        return self.cliente.nome_cliente
    
    @property
    def total(self):

        '''
        Essa função tem a propriedade de realizar o calculo matematico ligado ao total da soma do pedido realizado pelo Cliente
        '''
        queryset= self.itens.all().aggregate(
            total=models.Sum(models.F('quantidade') * models.F('produto__preco_unitario'))
        )

        return queryset['total']
                                   

class ItensPedido(models.Model):

    '''
    Essa entidade representa os itens pedidos pelo meu cliente, ou seja, os itens dentro de cada pedido realizado pelo cliente

    params: pedido (fk): é uma chave estrangeira que herda os atributos da minha Classe pedidos relacionada aos itens do pedido
    params: produto(fk): é uma chave estrangeira que herda os atributos da minha Classe Produto
    params: quantidade (int): representa a quantidade de itens que meu cliente vai adquirir

    '''
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='+') # o pedido pode ser apagado mas o produto nao
    quantidade = models.IntegerField()
    


class Pagamento(models.Model):

    '''
    Essa entidade representa a parte final da minha compra sendo ela o Pagamento.

    params: id_pagamento (pk): chave primária
    params: pedido (fk): chave estrangeira que herda os pedidos realizados pelo cliente
    params: status_pagamento (char): representa o estado do pagamento do cliente na hora de finalizar sua compra
    params: data_pagamento (date): data que foi realizado o pagamento do cliente
    '''
    id_pagamento = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    status_pagamento = models.CharField(
        max_length=20,
        choices= [('naorealizado','Não realizado'),('realizado','Realizado'),('emandamento','Em andamento'),('recusado','Recusado')],
        default= 'naorealizado'
    )
    data_pagamento = models.DateTimeField(auto_now_add=True)




    

    
