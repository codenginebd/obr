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
    name_2 = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)
    show_2 = models.BooleanField(default=False)
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

    @property
    def render_author_name_bn(self):
        return str(self.name_bn).decode('unicode_escape')

    @property
    def render_description_bn(self):
        return str(self.description_bn).decode('unicode_escape')

    def save(self):
        self.slug = slugify(self.name)
        try:
            self.create_thumbnail()
            # self.save()
        except Exception as msg:
            print("Thumbnail creation failed.")
        super(Author, self).save()


    def get_author_image_url(self):
        return settings.MEDIA_URL + '/' + str(self.thumbnail)
        
        
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
        
