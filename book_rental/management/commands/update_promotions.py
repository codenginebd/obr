from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

from enums import PromotionRewardTypes
from promotion.models.promotion import Promotion


class Command(BaseCommand):
    def handle(self, *args, **options):
        Promotion.objects.all().delete()

        print("Starting...")
        start_date = datetime.utcnow().date()
        end_date = start_date + timedelta(days=5)
        instance = Promotion.create_or_update_promotion(title="Test Promo",
                                                        description="Test Promo Desc",
                                                        start_date=start_date, end_date=end_date,
                                                        promotion_type="BUY",
                                                        by_cart_products_dates="BY_CART",
                                                        by_amount_qty="BY_AMOUNT",
                                                        min_qty_amount=100,
                                                        products=[(1,"Book", 50)],
                                                        rewards=[(PromotionRewardTypes.AMOUNT_IN_MONEY.value,
                                                                 False, 200, None, None, [(1,"Book", 50)])])
        if instance:
            print("Created.")
            print(instance.pk)
        for p in Promotion.objects.all():
            print(p.title)
        print("Ended.")