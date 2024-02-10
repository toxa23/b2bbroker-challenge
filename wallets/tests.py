from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class WalletModelTestCase(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label='Test Wallet', balance=100)

    def test_wallet_balance(self):
        self.assertEqual(self.wallet.balance, 100)

    def test_transaction_changes_balance(self):
        transaction = Transaction.objects.create(wallet=self.wallet, txid='12345', amount=50)
        self.assertEqual(self.wallet.balance, 150)
        transaction.delete()
        self.assertEqual(self.wallet.balance, 100)


class WalletAPIViewTestCase(APITestCase):
    def setUp(self):
        self.wallet_data = {'label': 'Test Wallet', 'balance': 100}
        self.wallet = Wallet.objects.create(label='Test Wallet', balance=100)

    def test_create_wallet(self):
        url = reverse('wallet-list')
        response = self.client.post(url, self.wallet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 2)

    def test_get_wallet_list(self):
        url = reverse('wallet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['label'], 'Test Wallet')


class TransactionAPIViewTestCase(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(label='Test Wallet', balance=100)
        self.first_transaction = Transaction.objects.create(wallet=self.wallet, txid='67890', amount=200)

    def test_create_transaction(self):
        url = reverse('transaction-list', kwargs={'wallet_id': self.wallet.id})
        transaction_data = {'wallet': self.wallet.id, 'txid': '12345', 'amount': 50}
        response = self.client.post(url, transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.transactions.count(), 2)
        self.assertEqual(self.wallet.balance, 350)

    def test_get_transaction_list(self):
        url = reverse('transaction-list', kwargs={'wallet_id': self.wallet.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['txid'], self.first_transaction.txid)

    def test_get_transaction_details(self):
        transaction = Transaction.objects.create(wallet=self.wallet, txid='12345', amount=50)
        url = reverse('transaction-detail', kwargs={'wallet_id': self.wallet.id, 'pk': transaction.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['txid'], '12345')
