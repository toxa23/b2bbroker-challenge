from django.urls import path
from .views import WalletList, WalletDetail, TransactionList, TransactionDetail

urlpatterns = [
    path('wallets', WalletList.as_view(), name='wallet-list'),
    path('wallets/<int:pk>', WalletDetail.as_view(), name='wallet-detail'),
    path('wallets/<int:wallet_id>/transactions', TransactionList.as_view(), name='transaction-list'),
    path('wallets/<int:wallet_id>/transactions/<int:pk>', TransactionDetail.as_view(), name='transaction-detail'),
]
