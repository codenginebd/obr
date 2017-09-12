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
    currency = models.ForeignKey(Currency)
    
    """
    credit_amount = 100.00
    credit_type = TRANSACTION_TYPES.CREDIT_STORE.value,
    
    """
    
    
    def add_credit(self, credit_amount, credit_type, expiry_time=None, **kwargs):
        
        if credit_type == TRANSACTION_TYPES.CREDIT_STORE.value:
            if not expiry_time:
                return None
        try:
            with transaction.atomic():
                self.total_credit += credit_amount
                self.save()
                credit_breakdown_instance = WalletCreditBreakdown()
                credit_breakdown_instance.credit_amount = credit_amount
                if credit_type == TRANSACTION_TYPES.CREDIT_STORE.value:
                    credit_breakdown_instance.credit_amount = expiry_time
                    credit_breakdown_instance.store_credit = True
                else:
                    credit_breakdown_instance.store_credit = False
                credit_breakdown_instance.save()
                self.credits.add(credit_breakdown_instance)
                return self
        except Exception as exp:
            return None
        
        
    def get_currency_code(self):
        return self.currency.short_name
        
    
    @classmethod
    def get_payment_wallet(cls, user_id, currency_code):
        payment_wallet_objects = cls.objects.filter(user_id=user_id, currency__short_name=currency_code)
        if payment_wallet_objects.exists():
            return payment_wallet_objects.first()
        return None
    
    
    @classmethod
    def create_or_update_payment_wallet(cls, user_id, currency_code, **kwargs):
        try:
            
            currency_objects = Currency.objects.filter(short_name=currency_code)
            if not currency_objects.exists():
                return None
                
            currency_object = currency_objects.first()
        
            pk = kwargs.get("pk")
            if pk:
                payment_wallet_objects = cls.objects.filter(pk=pk)
                if payment_wallet_objects.exists():
                    payment_wallet_object = payment_wallet_objects.first()
                else:
                    return None
            else:
                payment_wallet_object = cls()
            
            with transaction.atomic():
                payment_wallet_object.user_id = user_id
                payment_wallet_object.currency_id = currency_object.pk
                payment_wallet_object.save()
                
                return payment_wallet_object
            
        except Exception as exp:
            return None