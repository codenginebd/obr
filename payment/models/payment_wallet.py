from django.contrib.auth.models import User
from django.db import models
from generics.models.base_entity import BaseEntity
from payment.models.credit_breakdown import WalletCreditBreakdown
from payment.models.credit_payment_history import CreditPayHistory
from payment.models.currency import Currency


class PaymentWallet(BaseEntity):
    user = models.ForeignKey(User)
    total_credit = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    credits = models.ManyToManyField(WalletCreditBreakdown)
    payment_history = models.ManyToManyField(CreditPayHistory)
    currency = models.ForeignKey(Currency)
    
    
    @classmethod
    def create_or_update_payment_wallet(cls, user_id, currency_code, **kwargs):
        try:
            pk = kwargs.get("pk")
            if pk:
                pass
            else:
                pass
        except Exception as exp:
            pass