from django.conf import settings
from django.db import models
from django.db.models.query_utils import Q
from django.urls.base import reverse
import os
from bauth.models.address import Address
from bauth.models.email import Email
from bauth.models.phone import Phone
from book_rental.libs.downloader.publisher_downloader import PublisherDownloader
from book_rental.libs.uploader.publisher_uploader import PublisherUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader
from generics.mixin.thumbnail_model_mixin import ThumbnailModelMixin
from generics.models.base_entity import BaseEntity


class BookPublisher(BaseEntity, ThumbnailModelMixin):
    name = models.CharField(max_length=500)
    name_2 = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)
    show_2 = models.BooleanField(default=False)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    phones = models.ManyToManyField(Phone)
    emails = models.ManyToManyField(Email)
    image = models.ImageField(max_length=500, upload_to='publisher/', null=True)
    thumbnail = models.ImageField(max_length=500, upload_to='publisher/thumbnails/', null=True)

    def render_name(self):
        if self.name_2 and self.show_2:
            return self.name_2 + " (%s)" % self.name
        if self.name_2:
            return self.name + " (%s)" % self.name_2

    def render_thumbnail(self):
        if self.thumbnail:
            return os.path.join(settings.MEDIA_URL, self.thumbnail.name)
        else:
            return os.path.join(settings.STATIC_URL, 'images', 'author_no_avater.png')

    def save(self):
        try:
            self.create_thumbnail()
            # self.save()
        except Exception as msg:
            print("Thumbnail creation failed.")
        super(BookPublisher, self).save()

    @classmethod
    def show_create(cls):
        return True

    @classmethod
    def show_edit(cls):
        return True

    @classmethod
    def show_delete(cls):
        return True

    @classmethod
    def show_activate(cls):
        return True

    @classmethod
    def show_deactivate(cls):
        return True

    def get_emails(self):
        emails = self.emails.values_list('email', flat=True)
        return ','.join(emails)

    def get_phones(self):
        phones = self.phones.values_list('number', flat=True)
        return ','.join(phones)

    @classmethod
    def get_download_headers(cls):
        return ["Code", "Name(English)", "Name(Bangla)", "description(English)", "description(Bangla)", "Show Bangla"]

    @classmethod
    def get_download_template_headers(cls):
        return ["Code", "Name(English)", "Name(Bangla)", "description(English)",
                "description(Bangla)", "Show Bangla", "Image", "Email(s)", "Phone(s)"]

    @classmethod
    def get_table_headers(cls):
        return [
            "ID", "Code", "Name(English)", "Name(Bangla)", "Active?", "Show Bangla", "Details"
        ]

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

    @classmethod
    def prepare_download_template_data(cls, queryset):
        template_data = []
        for q_object in queryset:
            template_data += [[q_object.code, q_object.name, q_object.name_2, q_object.description, q_object.description_2,
                               "1" if q_object.show_2 else "0", q_object.image.name if q_object.image else '',
                               q_object.get_emails(), q_object.get_phones()]]
        return template_data

    @classmethod
    def get_downloader_class(cls):
        return PublisherDownloader

    @classmethod
    def get_download_file_name(cls):
        return "Publisher List"

    @classmethod
    def get_reader_class(cls):
        return ExcelFileReader

    @classmethod
    def get_uploader_class(cls):
        return PublisherUploader

    @classmethod
    def get_download_link(cls):
        return reverse("admin_book_publisher_download_view")

    @classmethod
    def get_upload_link(cls):
        return reverse("admin_book_publisher_upload_view")

    @classmethod
    def get_activate_link(cls):
        return reverse("admin_book_publisher_activate_view")

    @classmethod
    def get_deactivate_link(cls):
        return reverse("admin_book_publisher_deactivate_view")

    @classmethod
    def get_delete_link(cls):
        return reverse("admin_book_publisher_delete_view")

    @classmethod
    def get_detail_link(cls, object_id):
        return reverse("admin_book_publisher_details_view", kwargs={'pk': object_id})

    @classmethod
    def get_create_link(cls):
        return reverse("admin_book_publisher_create_view")

    @classmethod
    def get_edit_link_name(cls):
        return "admin_book_publisher_edit_link_view"

    @classmethod
    def get_edit_link(cls, object_id):
        return reverse("admin_book_publisher_edit_link_view", kwargs={"pk": object_id})

    @classmethod
    def get_search_by_options(cls):
        search_by_options = super(BookPublisher, cls).get_search_by_options()
        search_by_options += [
            ("By Name", "name")
        ]
        return search_by_options

    @classmethod
    def apply_search_filters(cls, request, queryset=None):
        queryset = super(BookPublisher, cls).apply_search_filters(request, queryset=queryset)
        name = request.GET.get("name", None)
        if name:
            queryset = queryset.filter(Q(name__icontains=name) | Q(name_2__icontains=name))
        return queryset