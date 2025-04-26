from django.db import models
from django.contrib.auth.models import User

# -------------------------------- CRIANDO AS ENTIDADES -------------------------------- #


class Cliente(models.Model):

    '''
    Entidade Cliente: representa os clientes do meu sistema.

    attr: id_cliente(pk) = chave única.
    attr: user(onetoone) = herda funcoes da classe User do Django.
    attr: nome_cliente(char) = nome do cliente.
    attr: cnpj(char) = campo opcional, caso seja uma pessoa juridica. 
    '''

    id_cliente = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_cliente = models.CharField(max_length=100, blank=False)
    cnpj = models.CharField(max_length=14, blank=True)


    # Representação do meu object dentro da tabela: nome do cliente
    def __str__(self):
        return self.nome_cliente

class Produto(models.Model):

    '''
    Entidade Produto: representa os produtos do meu sistema.

    attr: id_produto(pk) = chave única.
    attr: nome_produto(char) = nome do produto.
    attr: preco_unitario(decimal) = valor único por produto.
    attr: quantidade(int) = quantidade do produto disponível.
    attr: descricao(txt) = campo que contém a descrição do produto.
    '''
    
    id_produto = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=100, blank=False)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    descricao = models.TextField()


    # Representação do meu object dentro da tabela: nome do produto
    def __str__(self):
        return self.nome_produto
    
    def save(self, *args, **kwargs):

        '''
        Essa função permite eu verificar se o produto já existe e se o preço foi alterado.\n
        Ele só compara se o produto já existe no banco e aciona a minha task para envio de mail.
        '''
        
        if self.pk:  
            old_price = Produto.objects.get(pk=self.pk).preco_unitario
            if old_price != self.preco_unitario:  
                from sistema_pagamentos.tasks import enviar_email 
                enviar_email.delay(self.id_produto)
        super(Produto, self).save(*args, **kwargs)
    

class Pedido(models.Model):

    '''
    Entidade Pedido: representa os Pedidos realizados pelos clientes.

    attr: id_pedido(pk) = chave única.
    attr: cliente(fk) = chave estrangeira que herda os atributos da minha entidade Cliente.
    '''

    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')

    # Representação do meu object dentro da tabela: pedido relacionado ao nome do cliente
    def __str__(self):
        return self.cliente.nome_cliente
    

    @property
    def total(self):

        '''Permite realizar a soma total do valor do pedido feito pelo cliente.'''

        queryset= self.itens.all().aggregate(
            total=models.Sum(models.F('quantidade') * models.F('produto__preco_unitario'))
        )

        return queryset['total']
                                   

class ItensPedido(models.Model):

    '''
    Entidade ItensPedido: representa os itens de um pedido.

    attr: pedido(fk) = chave estrangeira que está relacionada ao pedido, herdando os atributos.
    attr: produto(fk) = chave estrangeira que herda os atributos da minha entidade Produto.
    attr: quantidade(int) = representa a quantidade de produtos que o cliente vai solicitar.
    '''
    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_pedido') 
    quantidade = models.IntegerField()
    


class Pagamento(models.Model):

    '''
    Entidade Pagamento: representa o estado final da compra realizada pelo client e.

    attr: id_pagamento(pk) = chave única.
    attr: pedido(fk) = chave estrangeira que herda os atributos do pedido feito pelo cliente.
    attr: status_pagamento(char) = estado do pagamento realizado pelo cliente: 'Não realizado', 'Realizado', 'Em andamento', 'Recusado'.
    attr: data_pagamento(date) = data da compra quando realizada.
    '''

    id_pagamento = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    status_pagamento = models.CharField(
        max_length=20,
        choices= [('naorealizado','Não realizado'),('realizado','Realizado'),('emandamento','Em andamento'),('recusado','Recusado')],
        default= 'naorealizado'
    )
    data_pagamento = models.DateTimeField(auto_now_add=True)




    

    
