from django.db import models

# O Django vai manipular essas informações com o ORM. 
# Representação das informações do Banco de Dados.

#Models

## Inserir lógica para o banco de dados [ não feita ]
## Evitar redundância no modelo atraves do @property [ em andamento ]

# Entidade Cliente, dados da pessoa ou da empresa.
# Cada cliente pode fazer vários pedidos e pode ter preços personalizdos para produtos através da tabela de preços.
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome_cliente = models.CharField(max_length=100,blank=False)
    email_cliente = models.EmailField(max_length=50,blank=False)
    CNPJ = models.CharField(max_length=14,unique=True, blank=True)

    # Representando objeto cliente como tipo string.
    def __str__(self):
        return self.nome_cliente

# Entidade Produto, especificações do produto. 
# Cada produto tem um preço base e pode estar em diferentes pedidos e vendas.
class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=50, blank=False)
    preco_padrao = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    descricao_produto = models.TextField(blank=False)
    data_validade_produto = models.DateField()

    # Retorna o objeto nome do produto.
    def __str__(self):
        return self.nome_produto
    
# Entidade Estoque, para armazenar os produtos. 
# Controla a quantidade de produtos disponíveis no estoque, além de manter registros de quando os produtos entram e saem do estoque.
class Estoque(models.Model):
    id_estoque = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_disponivel = models.IntegerField(default=0)
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(null=True, blank=True)
    
# Entidade Pedido, representa a solicitação de compra do cliente.
# Serve como um registro inicial de compras, antes da venda ser finalizada. O status de um pedido pode mudar com base no processo de pagamento e venda.
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)
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
    
# Entidade de Tabela de Preços, serve para armazenar os preços personalizados dos produtos para clientes específicos.
# Permite fornecer preços diferenciados para diferentes clientes
class TabelaPreco(models.Model):
    id_tabela = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_personalizado = models.DecimalField(max_digits=10, decimal_places=2)

    # Retorna o preço personalizado para o determinado cliente
    def __str__(self):
        return f'Preço personalizado para {self.cliente.nome_cliente} para produto {self.produto.nome_produto}, valor atualizado: {self.preco_personalizado} '

# Entidade Pagamento, representa o pagamento feito para um pedido.
# Controla detalhes do pagamento, como método (cartão, boleto, etc.) status do pagamento (pendente, aprovado, recusado) e data de processamento.
class Pagamento(models.Model):
    id_pagamento = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
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

    # Retorna o objeto do pagamento e pedido
    def __str__(self):
        return f"Pagamento {self.id_pagamento} - Pedido {self.pedido.id_pedido}"
    
# Entidade Venda, representa a transação concluída após o pagamento do pedido.
# A venda é a finalização do processo de compra, onde o pagamento confirmado e o produto foi entregue ou está pronto para entrega.
class Venda(models.Model):
    id_venda = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE) # Quando um cliente for excluído, todos os pedidos associados a esse cliente também serão excluídos automaticamente
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
    
# Passivel de remocao    
# Entidade Item de Venda, representa um produto específico que foi comprado em uma venda.
# Contém detalhes como a quantidade comprada e o preco unitário no momento da compra.
class HistoricoCompra(models.Model):
    id_historico = models.AutoField(primary_key=True)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    
    @property
    def exibir_cliente(self):
        return self.venda.cliente.nome_cliente
    
    @property
    def exibir_produto(self):
        return self.venda.pedido.produto.nome_produto

    @property
    def valor_produto(self):
        return self.venda.pedido.produto.preco_padrao

    @property
    def metodo_pagamento(self):
        return self.venda.pagamento.metodo_pagamento

    # Retorna o nome e a quantidade do produto vendida
    def __str__(self):
        return f'{self.venda.pedido.produto.nome_produto}'

