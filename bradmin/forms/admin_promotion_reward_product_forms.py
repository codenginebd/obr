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
        id = self.data.get(prefix + "-reward_id")
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
            pass
        else:
            return True
        return True
        
    

