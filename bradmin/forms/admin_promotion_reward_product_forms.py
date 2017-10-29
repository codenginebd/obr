from decimal import Decimal
from django import forms
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.fields.product_model_choice_field import ProductModelChoiceField
from enums import PromotionRewardTypes
from promotion.models.promotion_reward_products import PromotionRewardProduct


class AdminPromotionRewardProductForm(BRBaseModelForm):

    reward_product_id = forms.IntegerField(widget=forms.HiddenInput())

    reward_product = ProductModelChoiceField(label="Select Product",
                                      queryset=Book.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control"}))

    reward_is_new = forms.BooleanField(label="Is New")

    reward_print_type = forms.ChoiceField(label="Printing Type",
                                   choices=(("ECO", "Economy"), ("COL", "Color"), ("ORI", "Original")),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.reward_form_prefix = kwargs.pop('reward_form_prefix', None)
        super(AdminPromotionRewardProductForm, self).__init__(*args, **kwargs)
        self.fields["quantity"].widget.attrs["class"] = "form-control"

    class Meta:
        model = PromotionRewardProduct
        fields = ['reward_product_id', 'reward_product', 'reward_is_new', 'reward_print_type', 'quantity']

    def is_valid(self):
        self.error_messages = []
        self.cleaned_data = {}
        prefix = self.prefix
        reward_form_prefix = self.reward_form_prefix
        reward_form_index = prefix[:prefix.rindex("-")]
        reward_form_index = reward_form_index[reward_form_index.rindex("-") + 1:]
        reward_form_index = int(reward_form_index)
        reward_form_prefix += "-%s" % reward_form_index
        reward_type = self.data.get(reward_form_prefix + "-reward_type", None)
        try:
            reward_type = int(reward_type)
        except:
            self.error_messages += ["Reward type invalid"]
            return False
        if reward_type == PromotionRewardTypes.FREE_PRODUCTS.value or reward_type == PromotionRewardTypes.ACCESSORIES.value:
            reward_product_id = self.data.get(prefix + "-reward_product_id")
            reward_product = self.data.get(prefix + "-reward_product")
            reward_is_new = self.data.get(prefix + "-reward_is_new")
            reward_print_type = self.data.get(prefix + "-reward_print_type")
            quantity = self.data.get(prefix + "-quantity")
            if not reward_product or not reward_is_new or not reward_print_type or not quantity:
                self.error_messages += \
                    ["Product, Is New, Print Type and Quantity are all required in Reward Product"]
                return False
            try:
                if reward_product_id:
                    reward_product_id = int(reward_product_id)
                else:
                    reward_product_id = None
            except:
                self.error_messages += ["Invalid Reward Product Id"]
                return False
            try:
                reward_product = int(reward_product)
                reward_product = Book.objects.get(pk=reward_product)
            except:
                self.error_messages += ["Invalid Product Id in Reward Product"]
                return False
            reward_is_new = False if not reward_is_new else False
            try:
                quantity = Decimal(quantity)
            except:
                self.error_messages += ["Invalid quantity in Reward Product"]
                return False
            self.cleaned_data["id"] = reward_product_id
            self.cleaned_data["product"] = reward_product
            self.cleaned_data["is_new"] = reward_is_new
            self.cleaned_data["print_type"] = reward_print_type
            self.cleaned_data["quantity"] = quantity
            return True
        else:
            return True
        return True

    def save(self, **kwargs):
        if not self.cleaned_data.get("product"):
            return None
        if self.cleaned_data.get("id"):
            reward_product_instance = PromotionRewardProduct.objects.get(pk=id)
        else:
            reward_product_instance = PromotionRewardProduct()

        reward_product_instance.product_id = self.cleaned_data["product"].pk
        reward_product_instance.product_model = self.cleaned_data["product"].__class__.__name__
        reward_product_instance.is_new = self.cleaned_data["is_new"]
        reward_product_instance.print_type = self.cleaned_data["print_type"]
        reward_product_instance.quantity = self.cleaned_data["quantity"]
        reward_product_instance.save()
        return reward_product_instance
    

