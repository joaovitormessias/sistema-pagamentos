"""Regression coverage for order writes, notifications and report authorization."""
from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from .models import Cliente, Produto, Pedido, ItensPedido
from .serializer import CriarEditarPedidoSerializer, PagamentoSerializer
from .tasks import enviar_email


class WorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('demo', email='demo@example.com')
        self.customer = Cliente.objects.create(user=self.user, nome_cliente='Demo')
        self.product = Produto.objects.create(nome_produto='Tool', preco_unitario=100, quantidade=10, descricao='Demo')
        self.order = Pedido.objects.create(cliente=self.customer)
        ItensPedido.objects.create(pedido=self.order, produto=self.product, quantidade=2)

    def test_patch_replaces_items_without_duplicates(self):
        data = {'itens': [{'produto': self.product.pk, 'quantidade': 3}]}
        for _ in range(2):
            serializer = CriarEditarPedidoSerializer(self.order, data=data, partial=True)
            self.assertTrue(serializer.is_valid(), serializer.errors)
            serializer.save()
        self.assertEqual(self.order.itens.count(), 1)
        self.assertEqual(self.order.total, Decimal('300'))

    def test_patch_can_omit_items_and_empty_list_clears_them(self):
        serializer = CriarEditarPedidoSerializer(self.order, data={}, partial=True)
        self.assertTrue(serializer.is_valid()); serializer.save()
        self.assertEqual(self.order.itens.count(), 1)
        serializer = CriarEditarPedidoSerializer(self.order, data={'itens': []}, partial=True)
        self.assertTrue(serializer.is_valid()); serializer.save()
        self.assertEqual(self.order.total, Decimal('0'))

    def test_negative_order_quantity_rejected(self):
        serializer = CriarEditarPedidoSerializer(data={'cliente': self.customer.pk, 'itens': [{'produto': self.product.pk, 'quantidade': -1}]})
        self.assertFalse(serializer.is_valid())

    def test_payment_accepts_order(self):
        serializer = PagamentoSerializer(data={'pedido': self.order.pk, 'status_pagamento': 'realizado'})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.save().pedido, self.order)

    @patch('sistema_pagamentos.tasks.enviar_email.delay')
    def test_price_decrease_dispatched_after_commit(self, delay):
        with self.captureOnCommitCallbacks(execute=True) as callbacks:
            self.product.preco_unitario = Decimal('90')
            self.product.save()
            delay.assert_not_called()
            self.assertEqual(Produto.objects.get(pk=self.product.pk).preco_unitario, Decimal('90'))
        self.assertEqual(len(callbacks), 1)
        delay.assert_called_once_with(self.product.pk)

    @patch('sistema_pagamentos.tasks.enviar_email.delay')
    def test_price_increase_does_not_notify(self, delay):
        with self.captureOnCommitCallbacks(execute=True):
            self.product.preco_unitario = Decimal('110'); self.product.save()
        delay.assert_not_called()

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_repeat_buyer_receives_one_email(self):
        from django.core import mail
        ItensPedido.objects.create(pedido=self.order, produto=self.product, quantidade=1)
        self.assertEqual(enviar_email(self.product.pk), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_report_requires_staff_and_existing_customer(self):
        client = APIClient()
        url = f'/api/relatorio_pedidos/{self.customer.pk}/'
        self.assertEqual(client.get(url).status_code, 401)
        client.force_authenticate(self.user)
        self.assertEqual(client.get(url).status_code, 403)
        self.user.is_staff = True; self.user.save()
        self.assertEqual(client.get(url).status_code, 200)
        self.assertEqual(client.get('/api/relatorio_pedidos/9999/').status_code, 404)
