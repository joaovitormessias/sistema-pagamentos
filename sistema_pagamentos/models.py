from django.db import models

# O Django vai manipular essas informações com o ORM. 
# Representação das informações do Banco de Dados.

#Models

class Cliente(models.Model):

    """
    Entidade Cliente. Pode realizar o pedido e pagamento de um ou mais produtos.\n
    Representa tanto uma pessoa ou uma empresa, caraterizada por:
        ID único cliente (pk).
        Nome do cliente (char).
        Email do cliente (email)
        CNPJ da empresa (char).
    """

    id_cliente = models.AutoField(primary_key=True)
    nome_cliente = models.CharField(max_length=100,blank=False)
    email_cliente = models.EmailField(max_length=50,blank=False)
    cnpj = models.CharField(max_length=14,blank=True)

    # Representando objeto cliente como tipo string.
    def __str__(self):
        return self.nome_cliente

class Produto(models.Model):

    """
    Entidade Produto. Cada produto tem um preço base e pode estar em diferentes pedidos e vendas.\n
    Apresenta detalhes do produto, como:
        ID do produto (pk).
        Nome do produto (char).
        Descrição do produto (text).
        Data de validade do produto (date).
    """
    id_produto = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=50, blank=False)
    preco_padrao = models.DecimalField(max_digits=10, decimal_places=2, blank=False) #
    descricao_produto = models.TextField(blank=False)
    data_validade_produto = models.DateField()

    # Retorna o objeto nome do produto.
    def __str__(self):
        return self.nome_produto
    

class Estoque(models.Model):

    """
    Entidade Estoque. Controla a quantidade de produtos disponíveis no estoque, além de manter registros de quando os produtos entram e saem do estoque.\n
    Representada por:
        Produto (fk).
        Quantidade de produto disponível (int).
        Data da entrada do produto (date).
        Data de saída do produto (date).
    """

    id_estoque = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    # preco_padrao = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    quantidade_disponivel = models.IntegerField(default=0)
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(null=True, blank=True)

    # Fornece o valor unitário de determindo produto
    @property
    def valor_unitario(self):
        return self.produto.preco_padrao #
    
class Pedido(models.Model):

    """
    Entidade Pedido. Representa a solicitação de compra de um cliente. Serve como um registro inicial de compras, antes da venda ser finalizada.\n 
    O status de um pedido pode mudar com base no processo de pagamento e venda. Atributos: 
        ID pedido (pk).
        Cliente que fez o pedido (fk).
        Produto (fk). pode ser substituida pelo produto_estoque e armazenar o preco padrao
        Quantidade do produto solicitado (int).
        Data do pedido (date).
        Status do pedido (char).
    """

    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True) #
    quantidade_pedido = models.IntegerField(default=0)
    data_pedido = models.DateField(auto_now_add=True)
    status_pedido = models.CharField(
        max_length=20,
        choices=[("naorealizado","Não realizado"),("pendente","Pendente"),("realizado","Realizado"),("cancelado","Cancelado")],
        default="naorealizado",
        blank=False
    )

    # Retorna o pedido realizado pelo cliente
    def __str__(self):
        return f'Pedido {self.id_pedido} - {self.cliente.nome_cliente}'
    
class Pagamento(models.Model):

    """
    Entidade Pagamento. Só pode ser acesada caso o cliente tenha pedidos. Controla detalhes do pagamento, como:
        Pedidos realizados pelo cliente. 
        Método do pagamento. 
        Quantidade de parcelas.
        Status do pagamento.
        Data de processamento do pagamento.
    """

    id_pagamento = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True)
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=[("cartao","Cartão"),("boleto","Boleto"),("pix","PIX"),("dinheiro","Dinheiro"),("transferencia","Transferência")],
        default="cartao",
        blank=False,
        null=True
    )
    quantidade_parcelas = models.CharField(
        max_length=10,
        choices = [('avista','Avista'),('duas','2x'),('tres','3x'),('quatro','4x'),('cinco', '5x'),('seis', '6x'),('sete','7x'),('oito', '8x'), ('nove','9x'),('dez','10x'),('onze', '11x'),('doze','12x')],
        default="avista",
        blank=False,
    )
    status_pagamento = models.CharField(
        max_length=20,
        choices=[("pendente","Pendente"),("aprovado","Aprovado"),("recusado","Recusado"),("cancelado","Cancelado")],
        default="pendente",
        blank=False
    )
    data_pagamento = models.DateTimeField(auto_now_add=True)

    # Define o valor total da soma dos pedidos do cliente
    @property
    def total_pedido(self):
        total = sum(pedido.quantidade_pedido * pedido.produto.preco_padrao for pedido in Pedido.objects.filter(cliente=self.pedido.cliente)) #
        return total
    
    # Lista de produtos pedidos pelo cliente
    @property
    def produtos_pedidos(self):
        return [pedido.produto.nome_produto for pedido in Pedido.objects.filter(cliente=self.pedido.cliente)]
    
    # Retorna o objeto do pagamento e pedido
    def __str__(self):
        return f"Pagamento {self.id_pagamento} - Pedido {self.pedido.id_pedido}"
    
class Venda(models.Model):

    """
    Entidade Veda. Representa a transação concluída após o pagamento do pedido. \n
    Mais usada como histórico dos pagamentos contendo os pedidos para caso seja alterada o preço de um produto no estoque. \n
    Atributos:
        Pedido (fk).
        Cliente (fk).
        Pagamento (fk)
        Data da venda (date).
    """

    id_venda = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE)
    data_venda = models.DateField(auto_now_add=True)
    status_venda = models.CharField(
        max_length=20,
        choices=[("pendente","Pendente"),("concluida","Concluída"),("cancelada","Cancelada")],
        default="pendente",
        blank=False
    )

    # Retorna o ID da venda e o nome do cliente
    def __str__(self):
        return f'Venda: {self.id_venda} - Cliente {self.cliente.nome_cliente}'
    

