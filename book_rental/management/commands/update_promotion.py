from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from enums import PromotionRewardTypes
from promotion.models.promotion import Promotion


class Command(BaseCommand):
    def handle(self, *args, **options):
        Promotion.objects.all().delete()
        print("Starting...")
        # Buy 1 get 1 for product id 1
        start_date = datetime.utcnow().date() + timedelta(days=5)
        end_date = start_date + timedelta(days=10)
        params = {
            "title": "Buy 1 Get 1 for Product 1",
            "description": "This offer is for product 1 only. Buy 1 item and get 1 item free",
            "start_date": start_date,
            "end_date": end_date,
            "promotion_type": "BUY",
            "by_cart_products_dates": "BY_PRODUCTS",
            "by_amount_qty": "BY_QTY",
            "min_qty_amount": 1,
            "currency_code": "BDT",
            "products": [(1, "Book", True, "ECO", 1)],
            "rewards": [(PromotionRewardTypes.FREE_PRODUCTS.value, None, None, None, None,
                         [(1, "Book", True, "ECO", 1)])]
        }
        instance = Promotion.create_or_update_promotion(**params)
        if instance:
            print("Done. Instance Id: %s" % instance.pk)

        # Buy product 2 min 3 items and get 1 item free
        start_date = datetime.utcnow().date() + timedelta(days=1)
        end_date = start_date + timedelta(days=10)
        params = {
            "title": "Buy 1 Get 1 for Product 1",
            "description": "This offer is for product 1 only. Buy 1 item and get 1 item free",
            "start_date": start_date,
            "end_date": end_date,
            "promotion_type": "BUY",
            "by_cart_products_dates": "BY_PRODUCTS",
            "by_amount_qty": "BY_QTY",
            "min_qty_amount": 1,
            "currency_code": "BDT",
            "products": [(2, "Book", True, "ECO", 3)],
            "rewards": [(PromotionRewardTypes.FREE_PRODUCTS.value, None, None, None, None,
                         [(2, "Book", True, "ECO", 1)])]
        }
        instance = Promotion.create_or_update_promotion(**params)
        if instance:
            print("Done. Instance Id: %s" % instance.pk)

        # Buy min 500 BDT and get free shipping
        start_date = datetime.utcnow().date()
        end_date = start_date + timedelta(days=30)
        params = {
            "title": "Buy 1 Get 1 for Product 1",
            "description": "This offer is for product 1 only. Buy 1 item and get 1 item free",
            "start_date": start_date,
            "end_date": end_date,
            "promotion_type": "BUY",
            "by_cart_products_dates": "BY_CART",
            "by_amount_qty": "BY_AMOUNT",
            "min_qty_amount": 500,
            "currency_code": "BDT",
            "products": [],
            "rewards": [(PromotionRewardTypes.FREE_SHIPPING.value, None, None, None, None,
                         [])]
        }
        instance = Promotion.create_or_update_promotion(**params)
        if instance:
            print("Done. Instance Id: %s" % instance.pk)