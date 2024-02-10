from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    instance.wallet.balance += instance.amount
    instance.wallet.save()


@receiver(post_delete, sender=Transaction)
def transaction_post_delete(sender, instance, **kwargs):
    instance.wallet.balance -= instance.amount
    instance.wallet.save()
