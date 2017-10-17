from django.db import models
from datetime import datetime
from django.db.models.query_utils import Q
from django.urls.base import reverse

from ecommerce.models.rent_plan import RentPlan
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation
from generics.libs.loader.loader import load_model
from generics.models.base_entity import BaseEntity
from payment.models.currency import Currency
from engine.clock.Clock import Clock


class PriceMatrixManager(models.Manager):
    def get_queryset(self):
        todays_datetime = datetime.now()
        todays_ts = Clock.convert_datetime_to_utc_timestamp(todays_datetime)    
        queryset = super(PriceMatrixManager, self).get_queryset()
        queryset = queryset.filter(Q(is_rent=False) | (Q(is_rent=True) & Q(offer_date_start__isnull=False) & Q(offer_date_start__lte=todays_ts) & Q(offer_date_end__isnull=False) & Q(offer_date_end__gte=todays_ts)))
        return queryset


class PriceMatrix(BaseEntity):
    rent_plans = models.ManyToManyField(RentPlan, through=RentPlanRelation)
    is_rent = models.BooleanField(default=False)
    offer_price_p = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in percentage
    offer_price_v = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # value in value
    special_price = models.BooleanField(default=False)
    offer_date_start = models.BigIntegerField(default=0)
    offer_date_end = models.BigIntegerField(default=0)
    product_code = models.CharField(max_length=20)
    product_model = models.CharField(max_length=100)
    is_new = models.IntegerField(default=0)
    print_type = models.CharField(max_length=50)  # COL, ORI, ECO
    base_price = models.DecimalField(max_digits=20, decimal_places=2)
    market_price = models.DecimalField(max_digits=20, decimal_places=2)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    initial_payable_rent_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    currency = models.ForeignKey(Currency)
    
    objects = PriceMatrixManager()
    
    class Meta:
        index_together = [ 'product_code', 'product_model', 'is_new', 'print_type' ]

    def get_product(self):
        if self.product_model == "Book":
            Book = load_model(app_label="book_rental", model_name="Book")
            book_objects = Book.objects.filter(code=self.code)
            if book_objects.exists():
                return book_objects.first()

    @classmethod
    def show_create(cls):
        return True

    @classmethod
    def get_create_link(cls):
        return reverse("admin_product_price_create_view")

    @classmethod
    def get_table_headers(self):
        return ["ID", "Code", "Product", "Is New", "Print Type", "Rent Available", "Details"]

    @classmethod
    def prepare_table_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [q_object.pk, q_object.code, q_object.get_product(),
                 "Yes" if q_object.is_new else "No", q_object.print_type,
                 "Yes" if q_object.is_rent else "No",
                 '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)]
            ]
        return data