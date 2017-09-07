from django.db import models
from django.template.defaultfilters import slugify
from ecommerce.models.sales.category import ProductCategory
from ecommerce.models.sales.keyword import TagKeyword
from ecommerce.models.sales.product_images import ProductImage
from generics.models.base_entity import BaseEntity
from ecommerce.models.sales.price_matrix import PriceMatrix
from engine.clock.Clock import Clock
from ecommerce.models.sales.rent_plan_relation import RentPlanRelation


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
                        'base_price': 100,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
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
                        'base_price': 100,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
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
                        'base_price': 100,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
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
                        'base_price': 100,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
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
                        'base_price': 100,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
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
                        'base_price': 100,
                        'special': True,
                        'special_price': 0.7,
                        'special_date_start': datetime,
                        'special_date_end': datetime,
                        'rent_price_available': True,
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
                        
                unit_prices['New'][instance.print_type] = {
                    'base_price': instance.base_price,
                    'market_price': instance.market_price,
                    'currency_code': instance.currency.short_name
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Product, self).save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)

    class Meta:
        abstract = True