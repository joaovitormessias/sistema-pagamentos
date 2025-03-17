from django.db import models

# O Django vai manipular essas informações com o ORM. 
# Representação das informações do Banco de Dados

#Models

# Entidade Cliente 
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome_cliente = models.CharField(max=100,blank=False)
    email_cliente = models.EmailField(max=50,blank=False)
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
    
# Entidade Condição de Pagamento
class CondicaoPagamento(models.Model):
    id_condicao = models.AutoField(primary_key=True)
    descricao = models.TextField()
    parcela = models.IntegerField(blank=True)
    juros = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    # Retorna o objeto da descrição do pagamento. Ex: '3x no cartão'
    def __str__(self):
        return self.descricao
    
class Venda(models.Model):
    id_venda = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE) # Quando um cliente for excluído, todos os pedidos associados a esse cliente também serão excluídos automaticamente
    condicao_pagamento = models.ForeignKey(CondicaoPagamento, on_delete=models.CASCADE)
    data_venda = models.DateField(auto_now_add=True)

    # Retorna o ID da venda e o nome do cliente
    def __str__(self):
        return f'Venda: {self.id_venda} - {self.cliente.nome_cliente}'
    
# Entidade Item de Venda
class itemVenda(models.Model):
    id_item = models.AutoField(primary_key=True)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_unitario = models.DecimalField(max_digits=10,decimal_places=2, blank= True)
    quantidade = models.IntegerField(blank=True)

    # Retorna o nome e a quantidade do produto vendida
    def __str__(self):
        return f'{self.produto.nome_produto} (Quantidade: {self.quantidade})'

# Entidade de Tabela de Preços
class tabelaPreco(models.Model):
    id_tabela = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_personalizado = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    # Retorna o preço personalizado para o determinado cliente
    def __str__(self):
        return f'Preço personalizado para {self.cliente.nome_cliente} para produto {self.produto.nome_produto}, valor atualizado: {self.preco_personalizado} '