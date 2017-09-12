from enum import Enum


class PROMOTION_REWARD_TYPES(Enum):
    AMOUNT_IN_MONEY = 0
    FREE_SHIPPING = 1
    FREE_PRODUCTS = 2
    ACCESSORIES = 3
    STORE_CREDIT = 4


class DISCOUNT_REWARD_TYPE(Enum):
    AMOUNT_IN_MONEY = 0
    FREE_SHIPPING = 1
    FREE_PRODUCTS = 2
    ACCESSORIES = 3
    STORE_CREDIT = 4


class PROMOTION_TYPES(Enum):
    BUY = 0
    RENT = 1

class TRANSACTION_TYPES(Enum):
    CREDIT_STORE = 0
    BUY = 1
    RENT = 2
    SALE = 3
    REFUND = 4
    RENT_RETURN = 5
    FAILED_RETURN = 6
    
    
class PAYMENT_METHODS(Enum):
    STORE_CREDIT = 0
    CASH_ON_DELIVERY = 1
    CARD_PAYMENT =2
    MOBILE_PAYMENT = 3
    ONLINE_PAYMENT = 4
    
    
class PAYMENT_STATUS(Enum):
    PENDING = 0
    PROCESSED = 1
    FAILED = 2
    CANCELLED = 3
    