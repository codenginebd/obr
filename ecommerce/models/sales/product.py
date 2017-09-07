from django.db import models
from django.template.defaultfilters import slugify
from ecommerce.models.sales.category import ProductCategory
from ecommerce.models.sales.keyword import TagKeyword
from ecommerce.models.sales.product_images import ProductImage
from generics.models.base_entity import BaseEntity
from ecommerce.models.sales.price_matrix import PriceMatrix


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
                        'rent_price_available': True,
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
                        'rent_price_available': True,
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
                        'rent_price_available': True,
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
                        'rent_price_available': True,
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
                        'rent_price_available': True,
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
                        'rent_price_available': True,
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
                }
            }
        """
        unit_prices = {}
        price_instances = PriceMatrix.objects.filter(product_model=self.__class__.__name__, product_code=self.code)
        if price_instances.exists():
            for instance in price_instances:
                if instance.is_new == 1:
                    if not 'New' in unit_prices.items():
                        unit_prices['New'] = {  }
                    if instance.print_type == 'ECO':
                        pass
                    elif instance.print_type == 'COL':
                        pass
                    elif instance.print_type == 'ORI':
                        pass
                else:
                    pass
        self.prices = unit_prices

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        super(Product, self).save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)

    class Meta:
        abstract = True