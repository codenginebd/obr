from django import forms
from bradmin.forms.base_model_form import BRBaseModelForm
from enums import PromotionRewardTypes
from promotion.models.promotion_reward import PromotionReward


class AdminPromotionRewardForm(BRBaseModelForm):

    reward_type = forms.ChoiceField(label="Reward Type",
                                   choices=(
                                       (PromotionRewardTypes.AMOUNT_IN_MONEY.value, "Amount In Money"),
                                       (PromotionRewardTypes.FREE_SHIPPING.value, "Free Shipping"),
                                       (PromotionRewardTypes.FREE_PRODUCTS.value, "Free Products"),
                                       (PromotionRewardTypes.ACCESSORIES.value, "Accessories"),
                                       (PromotionRewardTypes.STORE_CREDIT.value, "Store Credit")
                                   ),
                                   widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super(AdminPromotionRewardForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PromotionReward
        fields = ['reward_type', 'gift_amount', 'gift_amount_in_percentage', 'store_credit', 'credit_expiry_time']
        widgets = {

        }
        labels = {
        }


