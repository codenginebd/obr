from django.db import models
from enums import TransactionTypes, PaymentStatus
from generics.models.base_entity import BaseEntity


class WalletTransaction(BaseEntity):
    wallet = models.ForeignKey("PaymentWallet", on_delete=models.CASCADE)
    transaction_type = models.IntegerField(default=TransactionTypes.CREDIT_STORE.value)
    total = models.DecimalField(decimal_places=2, max_digits=20)
    transaction_status = models.IntegerField(default=PaymentStatus.PENDING.value)

    @classmethod
    def create_wallet_transaction(cls, wallet_id, transaction_type, total, transaction_status):
        tnx_instance = cls()
        tnx_instance.wallet_id = wallet_id
        tnx_instance.transaction_type = transaction_type
        tnx_instance.total = total
        tnx_instance.transaction_status = transaction_status
        tnx_instance.save()
        return tnx_instance
