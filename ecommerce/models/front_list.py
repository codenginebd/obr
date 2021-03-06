from django.db import models
from django.urls.base import reverse

from ecommerce.models.front_list_product import FrontListProduct
from ecommerce.models.front_palette import FrontPalette
from ecommerce.models.sales.category import ProductCategory
from generics.libs.loader.loader import load_model
from generics.models.base_entity import BaseEntity


class FrontList(BaseEntity):
    title = models.CharField(max_length=400)
    title_2 = models.CharField(max_length=400, null=True)
    show_2 = models.NullBooleanField(default=False, null=True)
    description = models.TextField(null=True)
    by_rule = models.NullBooleanField(default=False, null=True)
    category = models.ForeignKey(ProductCategory, null=True, on_delete=models.CASCADE)
    rule_name = models.CharField(max_length=100, null=True)  # FrontListRule.TOP_X_PTC_DISCOUNT.value
    top_limit = models.IntegerField(default=0, null=True)
    max_limit = models.IntegerField(default=0, null=True)
    exclude_products = models.ManyToManyField(FrontListProduct, related_name="Front_list_exclude_products")
    products = models.ManyToManyField(FrontListProduct)
    detail_url = models.CharField(max_length=200)
    palette = models.ForeignKey(FrontPalette, on_delete=models.CASCADE)


    def get_front_products(self):
        products = []
        if self.products.exists():
            product_model = self.products.first().product_model
            product_ids = self.products.values_list('product_id', flat=True)
            if product_model == "Book":
                Book = load_model(app_label="book_rental", model_name="Book")
                products = Book.objects.filter(pk__in=product_ids)
        product_list = ['<a class="front_product_class" href="%s">%s</a>' % (p.get_detail_link(object_id=p.pk), str(p)) for p in products]
        return ','.join(product_list)

    def get_exclude_products(self):
        products = []
        if self.exclude_products.exists():
            product_model = self.exclude_products.first().product_model
            product_ids = self.exclude_products.values_list('product_id', flat=True)
            if product_model == "Book":
                Book = load_model(app_label="book_rental", model_name="Book")
                products = Book.objects.filter(pk__in=product_ids)
        product_list = ['<a class="front_product_class" href="%s">%s</a>' % (p.get_detail_link(object_id=p.pk), str(p)) for p in products]
        return ','.join(product_list)


    def get_product_list(self):
        return []

    def populate_products(self):
        pass

    @classmethod
    def show_create(cls):
        return True

    @classmethod
    def show_edit(cls):
        return True

    @classmethod
    def show_activate(cls):
        return True

    @classmethod
    def show_deactivate(cls):
        return True

    @classmethod
    def show_delete(cls):
        return True

    @classmethod
    def get_create_link(cls):
        return reverse("admin_front_list_create_view")

    @classmethod
    def get_edit_link(cls, object_id):
        return reverse("admin_front_list_edit_link_view", kwargs={"pk": object_id})

    @classmethod
    def get_edit_link_name(cls):
        return "admin_front_list_edit_link_view"

    @classmethod
    def get_activate_link(cls):
        return reverse("admin_front_list_activate_view")

    @classmethod
    def get_deactivate_link(cls):
        return reverse("admin_front_list_deactivate_view")

    @classmethod
    def get_delete_link(cls):
        return reverse("admin_front_list_delete_view")

    @classmethod
    def get_detail_link(cls, object_id):
        return reverse("admin_front_list_details_view", kwargs={"pk": object_id})

    def get_object_detail_link(self):
        return reverse("admin_front_list_details_view", kwargs={"pk": self.pk})

    @classmethod
    def get_table_headers(self):
        return ["ID", "Code", "Title", "Title 2", "Show 2", "By Rule", "Rule Name", "Is Active", "Details"]

    @classmethod
    def prepare_table_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [q_object.pk, q_object.code, q_object.title, q_object.title_2,
                 "Yes" if q_object.show_2 else "No", "Yes" if q_object.by_rule else "No",
                 q_object.rule_name, "Yes" if q_object.is_active else "No",
                 '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)]
            ]
        return data