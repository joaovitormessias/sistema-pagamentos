from django.db import models

# O Django vai manipular essas informações com o ORM. 
# Representação das informações do Banco de Dados

#Models

# Entidade Cliente 
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome_cliente = models.CharField(max_length=100,blank=False)
    email_cliente = models.EmailField(max_length=50,blank=False)
    CNPJ = models.CharField(max_length=14,unique=True, blank=False)

    # Representando objeto cliente como tipo string
    def __str__(self):
        return self.nome_cliente

# Entidade Produto
class Produto(models.Model):
    id_produto = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=50, blank=True)
    preco_padrao = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    descricao_produto = models.TextField(blank=True)
    data_validade_produto = models.DateField()

    # Retorna o objeto nome do produto
    def __str__(self):
        return self.nome_produto
    
# Entidade Pedido
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateField(auto_now_add=True)
    status_pedido = models.CharField(
        max_length=20,
        choices=[("pendente","Pendente"),("realizado","Realizado"),("cancelado","Cancelado")],
        default="pendente",
        blank=True
    )

    # Retorna o pedido realizado pelo cliente
    def __str__(self):
        return f'Pedido {self.id_pedido} - {self.cliente.nome_cliente}'

# Entidade Condição de Pagamento
class Pagamento(models.Model):
    id_pagamento = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=[("cartao","Cartão"),("boleto","Boleto"),("pix","PIX"),("dinheiro","Dinheiro"),("transferencia","Transferência")],
        default="cartao",
        blank=True
    )
    status_pagamento = models.CharField(
        max_length=20,
        choices=[("pendente","Pendente"),("aprovado","Aprovado"),("recusado","Recusado"),("cancelado","Cancelado")],
        default="pendente",
        blank=True
    )
    data_pagamento = models.DateTimeField(null=True, blank=True)

    # Retorna o objeto do pagamento e pedido
    def __str__(self):
        return f"Pagamento {self.id_pagamento} - Pedido {self.pedido.id_pedido}"
    
# Entidade Venda
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
        blank=True
    )
    # Retorna o ID da venda e o nome do cliente
    def __str__(self):
        return f'Venda: {self.id_venda} - Cliente {self.cliente.nome_cliente}'
    
# Entidade Item de Venda
class ItemVenda(models.Model):
    id_item = models.AutoField(primary_key=True)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2, blank= True)
    quantidade = models.IntegerField(blank=True)

    # Retorna o nome e a quantidade do produto vendida
    def __str__(self):
        return f'{self.produto.nome_produto} (Quantidade: {self.quantidade})'

# Entidade de Tabela de Preços
class TabelaPreco(models.Model):
    id_tabela = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_personalizado = models.DecimalField(max_digits=10, decimal_places=2)

    # Retorna o preço personalizado para o determinado cliente
    def __str__(self):
        return f'Preço personalizado para {self.cliente.nome_cliente} para produto {self.produto.nome_produto}, valor atualizado: {self.preco_personalizado} '