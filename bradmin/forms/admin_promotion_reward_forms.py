from django import forms
from bradmin.forms.base_model_form import BRBaseModelForm
from enums import PromotionRewardTypes
from promotion.models.promotion_reward import PromotionReward


class AdminPromotionRewardForm(BRBaseModelForm):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())

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
        fields = ['id', 'reward_type', 'gift_amount', 'gift_amount_in_percentage', 'store_credit', 'credit_expiry_time']
        
    def is_valid(self):
        self.error_messages = []
        self.cleaned_data = {}
        prefix = self.prefix
        id = self.data.get(prefix + "-id")
        reward_type = self.data.get(prefix+"-reward_type")
        gift_amount = self.data.get(prefix+"-gift_amount")
        gift_amount_in_percentage = self.data.get(prefix+"-gift_amount_in_percentage")
        store_credit = self.data.get(prefix+"-store_credit")
        credit_expiry_time = self.data.get(prefix+"-credit_expiry_time")
        self.cleaned_data["reward_type"] = PromotionRewardTypes.FREE_SHIPPING.value
        if reward_type == PromotionRewardTypes.FREE_SHIPPING.value:
            self.cleaned_data["reward_type"] = reward_type
            return True
        elif reward_type == PromotionRewardTypes.AMOUNT_IN_MONEY.value:
            if gift_amount and gift_amount_in_percentage is not None:
                try:
                    gift_amount = Decimal(gift_amount)
                except:
                    self.error_messages += ["Gift amount should be a decimal number"]
                    return False
                gift_amount_in_percentage = 0 if not gift_amount_in_percentage else 1
                gift_amount_in_percentage = bool(gift_amount_in_percentage)
                self.cleaned_data["gift_amount"] = gift_amount
                self.cleaned_data["gift_amount_in_percentage"] = gift_amount_in_percentage
                return True
            else:
                self.error_messages += ["Either gift amount or gift amount in percentage missing"]
                return False
        elif reward_type == PromotionRewardTypes.FREE_PRODUCTS.value:
            return True
        elif reward_type == PromotionRewardTypes.ACCESSORIES.value:
            return True
        elif reward_type == PromotionRewardTypes.STORE_CREDIT.value:
            if store_credit and credit_expiry_time:
                try:
                    store_credit = Decimal(store_credit)
                except:
                    self.error_messages += ["Store Credit should be a decimal number"]
                    return False
                try:
                    credit_expiry_time = datetime.strptime("%m/%d/%Y", credit_expiry_time)
                except:
                    self.error_messages += ["Credit expiry date is invalid"]
                    return False
                self.cleaned_data["store_credit"] = store_credit
                self.cleaned_data["credit_expiry_time"] = credit_expiry_time
                return True
            else:
                self.error_messages += ["Either store credit or credit expiry date is missing"]
                return False
        return False
        
    def save(self, **kwargs):
        if self.cleaned_data.get("id"):
            promotion_reward_instance = PromotionReward.objects.get(pk=id)
        else:
            promotion_reward_instance = PromotionReward()
            
        promotion_reward_instance.reward_type = self.cleaned_data['reward_type']
        if self.cleaned_data.get("gift_amount"):
            promotion_reward_instance.gift_amount = self.cleaned_data['gift_amount']
        if self.cleaned_data.get("gift_amount_in_percentage"):
            promotion_reward_instance.gift_amount_in_percentage = self.cleaned_data['gift_amount_in_percentage']
        if self.cleaned_data.get("store_credit"):
            promotion_reward_instance.store_credit = self.cleaned_data['store_credit']
        if self.cleaned_data.get("credit_expiry_time"):
            promotion_reward_instance.credit_expiry_time = self.cleaned_data['credit_expiry_time']
        
        promotion_reward_instance.save()
        return promotion_reward_instance
        
                


