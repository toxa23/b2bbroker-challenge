from rest_framework import generics
from rest_framework.filters import OrderingFilter, BaseFilterBackend
from django_filters import rest_framework as filters
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from .filters import TransactionFilter


class WalletList(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('label', )


class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionFilter

    def get_queryset(self):
        wallet_id = self.kwargs.get('wallet_id')
        return Transaction.objects.filter(wallet_id=wallet_id)

    def perform_create(self, serializer):
        wallet_id = self.kwargs.get('wallet_id')
        wallet = Wallet.objects.get(pk=wallet_id)
        serializer.save(wallet=wallet)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        wallet_id = self.kwargs.get('wallet_id')
        return self.queryset.filter(wallet_id=wallet_id)
