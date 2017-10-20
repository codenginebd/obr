from django.db import models
from django.template.defaultfilters import slugify
from ecommerce.models.sales.category import ProductCategory
from ecommerce.models.sales.keyword import TagKeyword
from ecommerce.models.sales.product_images import ProductImage
from generics.libs.loader.loader import load_model
from generics.models.base_entity import BaseEntity
from engine.clock.Clock import Clock
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation

PriceMatrix = load_model(app_label="ecommerce", model_name="PriceMatrix")

class Product(BaseEntity):
    title = models.CharField(max_length=500)
    title_2 = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500)
    subtitle_2 = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)
    show_2 = models.BooleanField(default=False)
    categories = models.ManyToManyField(ProductCategory)
    sale_available = models.BooleanField(default=True)
    rent_available = models.BooleanField(default=False)
    tags = models.ManyToManyField(TagKeyword)
    mfg_date = models.IntegerField(default=0)
    expire_date = models.IntegerField(default=0)
    slug = models.SlugField()
    images = models.ManyToManyField(ProductImage)
    rating = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def get_category_codes(self):
        return ','.join(self.categories.values_list('code', flat=True))

    def get_image_names(self):
        return ','.join(self.images.values_list('image', flat=True))

    def get_tag_names(self):
        return ','.join(self.tags.values_list('name', flat=True))

    @classmethod
    def apply_search(cls, queryset, request=None, **kwargs):
        if request and request.GET.get('id'):
            search_criteria = int(request.GET.get('id'))
            queryset = queryset.filter(pk=search_criteria)
        return queryset
        
    def load_unit_prices(self):
        """
            Structure
            unit_prices = {
                'New': 
                {
                    'ECO': 
                    {
                        'market_price': 120,
                        'base_price': 100,
                        'sale_price': 40,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
                        'initial_payable_rent_price': 90
                        'currency_code': 'BDT',
                        'rent_prices': 
                        {
                            30: 
                            {
                                'base_price': 40,
                                'special': True,
                                'special_price': 0.6
                            }
                        }
                    },
                    'ORI': 
                    {
                        'market_price': 120,
                        'base_price': 100,
                        'sale_price': 40,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
                        'initial_payable_rent_price': 90
                        'currency_code': 'BDT',
                        'rent_prices': 
                        {
                            30: 
                            {
                                'base_price': 40,
                                'special': True,
                                'special_price': 0.6
                            }
                        }
                    },
                    'COL': 
                    {
                        'market_price': 120,
                        'base_price': 100,
                        'sale_price': 40,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
                        'initial_payable_rent_price': 90
                        'currency_code': 'BDT',
                        'rent_prices': 
                        {
                            30: 
                            {
                                'base_price': 40,
                                'special': True,
                                'special_price': 0.6
                            }
                        }
                    }
                },
                'Used': 
                {
                    'ECO': 
                    {
                        'market_price': 120,
                        'base_price': 100,
                        'sale_price': 40,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
                        'initial_payable_rent_price': 90
                        'currency_code': 'BDT',
                        'rent_prices': 
                        {
                            30: 
                            {
                                'base_price': 40,
                                'special': True,
                                'special_price': 0.6
                            }
                        }
                    },
                    'ORI': 
                    {
                        'market_price': 120,
                        'base_price': 100,
                        'sale_price': 40,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
                        'initial_payable_rent_price': 90
                        'currency_code': 'BDT',
                        'rent_prices': 
                        {
                            30: 
                            {
                                'base_price': 40,
                                'special': True,
                                'special_price': 0.6
                            }
                        }
                    },
                    'COL': 
                    {
                        'market_price': 120,
                        'base_price': 100,
                        'sale_price': 40,
                        'special': True,
                        'special_price': 70,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
                        'initial_payable_rent_price': 90
                        'currency_code': 'BDT',
                        'rent_prices': 
                        {
                            30: 
                            {
                                'base_price': 40,
                                'special': True,
                                'special_price': 0.6,
                                'special_date_start': datetime,
                                'special_date_end': datetime,
                            }
                        }
                    }
                }
            }
        """
        unit_prices = {}
        price_instances = PriceMatrix.objects.filter(product_model=self.__class__.__name__, product_code=self.code)
        if price_instances.exists():
            for instance in price_instances:
                usage_type = 'New'
                if instance.is_new == 1:
                    if not 'New' in unit_prices.items():
                        usage_type = 'New'
                else:
                    if not 'Used' in unit_prices.items():
                        usage_type = 'Used'
                        
                unit_prices[usage_type] = {  }
                        
                unit_prices[usage_type][instance.print_type] = {
                    'base_price': instance.base_price,
                    'market_price': instance.market_price,
                    'sale_price': instance.sale_price,
                    'currency_code': instance.currency.short_name,
                    'initial_payable_rent_price': instance.initial_payable_rent_price
                }
                unit_prices[usage_type][instance.print_type]['special'] = True if instance.special_price else False
                        
                if instance.special_price:
                    special_price_p = instance.offer_price_p
                        
                    unit_prices[usage_type][instance.print_type]['special_price'] = special_price_p * instance.base_price
                        
                    unit_prices[usage_type][instance.print_type]['special_date_start'] = Clock.convert_ts_to_datetime(instance.offer_date_start)
                    unit_prices[usage_type][instance.print_type]['special_date_end'] = Clock.convert_ts_to_datetime(instance.offer_date_end)
                    
                unit_prices[usage_type][instance.print_type]['rent_price_available'] = True if instance.is_rent else False
                
                if instance.is_rent:
                    rent_prices = {   }
                    
                    rent_plan_ids = instance.rent_plans.values_list('pk', flat=True)
                    
                    rent_plan_relation_objects = RentPlanRelation.objects.filter(plan_id__in=rent_plan_ids, price_matrix_id=instance.pk)
                    
                    for rp_instance in rent_plan_relation_objects:
                        if not rp_instance.pk in rent_prices.items():
                            rent_prices[rp_instance.pk] = {
                                'base_price': rp_instance.rent_rate * instance.base_price,
                                'special': True if rp_instance.is_special_offer else False
                            }
                            
                        if rp_instance.is_special_offer:
                            rent_prices[rp_instance.pk]['special_price'] = ( rp_instance.rent_rate * instance.base_price ) * rp_instance.special_rate
                            rent_prices[rp_instance.pk]['special_date_start'] = Clock.convert_ts_to_datetime(rp_instance.start_time)
                            rent_prices[rp_instance.pk]['special_date_end'] = Clock.convert_ts_to_datetime(rp_instance.end_time)
                        
                    unit_prices[usage_type][instance.print_type]['rent_prices'] = rent_prices
                    
        self._prices = unit_prices
        
    def get_price(self, is_new, print_type=None):
        prices = getattr(self, '_prices', None)
        if not prices:
            self.load_unit_prices()
            
        if is_new:
            new_prices = self._prices.get('New')
            if new_prices:
                if print_type:
                    return new_prices.get(print_type)
                return new_prices
        return None
        
    def get_base_price(self, is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('base_price')
        return None
        
    def get_market_price(self, is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('market_price')
        return None
        
    def get_sale_price(self, is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('sale_price')
        return None
        
    def get_sale_price(self, is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('sale_price')
        return None
        
    def get_initial_payable_rent_price(self, is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('initial_payable_rent_price')
        return None
        
    def check_rent_price_available(self,is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('rent_price_available')
        return None
        
    def get_currency_code(self,is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('currency_code')
        return None
        
    def check_special_price_available(self,is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('special')
        return None
        
    def get_special_price(self,is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('special_price')
        return None
        
    def get_effective_base_price(self,is_new, print_type):
        special = self.check_special_price_available(is_new=is_new, print_type=print_type)
        if special:
            return self.get_special_price(is_new=is_new, print_type=print_type)
        else:
            return self.get_base_price(is_new=is_new, print_type=print_type)
        
    def get_special_offer_start_date(self,is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('special_date_start')
        return None
        
    def get_special_offer_end_date(self,is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('special_date_end')
        return None
        
    def get_rent_prices(self,is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            return price_dict.get('rent_prices')
        return None
        
    def get_rent_price_options(self,is_new, print_type):
        price_dict = self.get_price(is_new=is_new, print_type=print_type)
        if price_dict:
            rent_prices = price_dict.get('rent_prices')
            if rent_prices:
                return rent_prices.keys()
        return None
        
    def get_rent_price_for_days(self,is_new, print_type, rent_days):
        rent_prices = self.get_rent_prices(is_new=is_new, print_type=print_type)
        if rent_prices:
            return rent_prices.get(rent_days)
        return None
        
    def get_base_rent_price_for_days(self,is_new, print_type, rent_days):
        rent_days_price = self.get_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
        if rent_days_price:
            return rent_days_price.get('base_price')
        return None
        
    def check_special_rent_price_for_days(self,is_new, print_type, rent_days):
        rent_days_price = self.get_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
        if rent_days_price:
            return rent_days_price.get('special')
        return None
        
    def get_special_rent_price_for_days(self,is_new, print_type, rent_days):
        rent_days_price = self.get_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
        if rent_days_price:
            return rent_days_price.get('special_price')
        return None
        
    def get_effective_rent_price_for_days(self,is_new, print_type, rent_days):
        special = self.check_special_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
        if special:
            return self.get_special_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
        else:
            return self.get_base_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
        
    def get_special_start_date_for_rent_days(self,is_new, print_type, rent_days):
        rent_days_price = self.get_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
        if rent_days_price:
            return rent_days_price.get('special_date_start')
        return None
        
    def get_special_end_date_for_rent_days(self,is_new, print_type, rent_days):
        rent_days_price = self.get_rent_price_for_days(is_new=is_new, print_type=print_type, rent_days=rent_days)
        if rent_days_price:
            return rent_days_price.get('special_date_end')
        return None

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Product, self).save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)

    class Meta:
        abstract = True