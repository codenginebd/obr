from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls.base import reverse

from bauth.models.address import Address
from bauth.models.country import Country
from bauth.models.email import Email
from bauth.models.phone import Phone
from book_rental.libs.downloader.author_downloader import AuthorDownloader
from book_rental.libs.uploader.author_uploader import AuthorUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader
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

    @classmethod
    def show_create(cls):
        return True

    @classmethod
    def show_edit(cls):
        return True

    @classmethod
    def show_download(cls):
        return True

    @classmethod
    def show_download_template(cls):
        return True

    @classmethod
    def show_upload(cls):
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
        return reverse("admin_author_create_view")

    @classmethod
    def get_detail_link(cls, object_id):
        return reverse("admin_author_details_view", kwargs={"pk": object_id})

    @classmethod
    def get_edit_link(cls, object_id):
        return reverse("admin_author_edit_link_view", kwargs={"pk": object_id})

    @classmethod
    def get_edit_link_name(cls):
        return "admin_author_edit_link_view"

    @classmethod
    def get_download_link(cls):
        return reverse("admin_author_download_view")

    @classmethod
    def get_upload_link(cls):
        return reverse("admin_author_upload_view")

    @classmethod
    def get_activate_link(cls):
        return reverse("admin_author_activate_view")

    @classmethod
    def get_deactivate_link(cls):
        return reverse("admin_author_deactivate_view")

    @classmethod
    def get_delete_link(cls):
        return reverse("admin_author_delete_view")

    @classmethod
    def get_downloader_class(cls):
        return AuthorDownloader

    @classmethod
    def get_uploader_class(cls):
        return AuthorUploader

    @classmethod
    def get_reader_class(cls):
        return ExcelFileReader

    @classmethod
    def get_download_file_name(cls):
        return "Author List"

    @classmethod
    def get_table_headers(cls):
        return [
            "ID", "Code", "Name", "Name 2", "Active?", "Show 2", "Details"
        ]

    @classmethod
    def get_download_headers(cls):
        return ["Code", "Author Name", "Author Name 2", "Is Active", "Show 2", "Date Of Birth(dd/mm/yyyy)"]

    @classmethod
    def get_download_template_headers(cls):
        return ["Code", "Author Name", "Author Name 2", "Author Description",
                "Author Description 2", "Show 2", "Author Image",
                "Date Of Birth(dd/mm/yyyy)", "Email(s)", "Phone(s)"]

    @classmethod
    def prepare_table_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.name, q_object.name_2, "Yes" if q_object.is_active else "No",
                    "Yes" if q_object.show_2 else "No",
                    '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)
                ]
            ]
        return data

    def get_emails(self):
        return ','.join(self.emails.values_list('email', flat=True))

    def get_phones(self):
        return ','.join(self.phones.values_list('number', flat=True))

    @classmethod
    def prepare_download_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.code, q_object.name, q_object.name_2, "Yes" if q_object.is_active else "No",
                    "Yes" if q_object.show_2 else "No",
                    q_object.date_of_birth.strftime("%d/%m/%Y") if q_object.date_of_birth else ""
                ]
            ]
        return data

    @classmethod
    def prepare_download_template_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.code, q_object.name, q_object.name_2, q_object.description, q_object.description_2,
                    "1" if q_object.show_2 else "0", q_object.image.name.replace("author/", "") if q_object.image else "",
                    q_object.date_of_birth.strftime("%d/%m/%Y") if q_object.date_of_birth else "",
                    q_object.get_emails(), q_object.get_phones()
                ]
            ]
        return data
