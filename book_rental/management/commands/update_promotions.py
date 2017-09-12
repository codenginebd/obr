from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

from promotion.models.promotion import Promotion


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting...")
        start_date = datetime.utcnow().date()
        end_date = start_date + timedelta(days=5)
        instance = Promotion.create_or_update_promotion(title="Test Promo",
                                                        description="Test Promo Desc",
                                                        start_date=start_date, end_date=end_date,
                                                        promotion_type="BUY",
                                                        by_cart_products_dates="BY_CART")
        if instance:
            print("Created.")
            print(instance.pk)
        print("Ended.")