from enum import Enum


class PromotionRewardTypes(Enum):
    AMOUNT_IN_MONEY = 0
    FREE_SHIPPING = 1
    FREE_PRODUCTS = 2
    ACCESSORIES = 3
    STORE_CREDIT = 4


class DiscountRewardTypes(Enum):
    AMOUNT_IN_MONEY = 0
    FREE_SHIPPING = 1
    FREE_PRODUCTS = 2
    ACCESSORIES = 3
    STORE_CREDIT = 4


class PromotionTypes(Enum):
    BUY = 0
    RENT = 1
    ANY = 2


class TransactionTypes(Enum):
    CREDIT_STORE = 0
    BUY = 1
    RENT = 2
    SALE = 3
    REFUND = 4
    RENT_RETURN = 5
    FAILED_RETURN = 6
    CREDIT_USE = 7
    
    
class PaymentMethods(Enum):
    STORE_CREDIT = 0
    CASH_ON_DELIVERY = 1
    CARD_PAYMENT =2
    MOBILE_PAYMENT = 3
    ONLINE_PAYMENT = 4
    
    
class PaymentStatus(Enum):
    PENDING = 0
    PROCESSED = 1
    FAILED = 2
    CANCELLED = 3


class InventoryTXNType(Enum):
    STOCK_IN = "STOCK_IN"
    STOCK_OUT = "STOCK_OUT"
    TNX_DB = "TNX_DB"
    TNX_CR = "TNX_CR"