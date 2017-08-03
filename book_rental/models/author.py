from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from bauth.models.address import Address
from bauth.models.country import Country
from bauth.models.email import Email
from bauth.models.phone import Phone
from generics.mixin.thumbnail_model_mixin import ThumbnailModelMixin
from generics.models.base_entity import BaseEntity
from generics.models.language import Language


class Author(BaseEntity, ThumbnailModelMixin):
    name = models.CharField(max_length=255, blank = True)
    description = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True)
    address = models.ForeignKey(Address, null=True)
    phones = models.ManyToManyField(Phone)
    rating = models.FloatField(default=0)
    emails = models.ManyToManyField(Email)
    image = models.ImageField(max_length=500, upload_to='author/', null=True)
    thumbnail = models.ImageField(max_length=500, upload_to='author/thumbnails/', null=True)
    nationalities = models.ManyToManyField(Country)
    languages = models.ManyToManyField(Language)
    slug = models.SlugField()

    def save(self):
        self.slug = slugify(self.name)
        try:
            self.create_thumbnail()
            # self.save()
        except Exception as msg:
            print("Thumbnail creation failed.")
        super(Author, self).save()
        
        
    @classmethod
    def get_all_authors(cls, product_cat=None, **kwargs):
        all_authors = cls.objects.none()
        if not product_cat:
            if kwargs.get('compact', False) == True:
                all_authors = cls.objects.all().values('id', 'name', 'slug', 'thumbnail')
            else:
                all_authors = cls.objects.all()
        else:
            pass
        return all_authors
        
