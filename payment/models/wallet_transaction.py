from django.db import models

class WalletTransaction(BaseEntity):
    wallet = models.ForeignKey(PaymentWallet)
    transaction_type = models.IntegerField(default=TRANSACTION_TYPES.CREDIT_STORE.value)
    total = models.DecimalField(decimal_places=2, max_digits=20)
    transaction_status = models.IntegerField(default=PAYMENT_STATUS.PENDING.value)
    
    
    @classmethod
    def create_wallet_transaction(cls, wallet_id, transaction_type, total, transaction_status):
        tnx_instance = cls()
        tnx_instance.wallet_id = wallet_id
        tnx_instance.transaction_type = transaction_type
        tnx_instance.total = total
        tnx_instance.transaction_status = transaction_status
        tnx_instance.save()
        return tnx_instance
        
        
        