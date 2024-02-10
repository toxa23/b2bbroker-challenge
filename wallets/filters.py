import django_filters
from django_filters.rest_framework import RangeFilter
from .models import Wallet, Transaction


class TransactionFilter(django_filters.FilterSet):
    amount = RangeFilter()

    class Meta:
        model = Transaction
        fields = ['amount']
