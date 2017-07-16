from django.contrib.auth.models import User
from django.db import models
from generics.models.base_entity import BaseEntity
from payment.models.credit_breakdown import WalletCreditBreakdown
from payment.models.credit_payment_history import CreditPayHistory


class PaymentWallet(BaseEntity):
    user = models.ForeignKey(User)
    total_credit = models.DecimalField(max_digits=20, decimal_places=2)
    credits = models.ManyToManyField(WalletCreditBreakdown)
    payment_history = models.ManyToManyField(CreditPayHistory)