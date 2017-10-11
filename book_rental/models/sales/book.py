from django.db import models
from django.db.models.query_utils import Q
from django.urls.base import reverse

from book_rental.libs.downloader.book_downloader import BookDownloader
from book_rental.libs.uploader.book_uploader import BookUploader
from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher
from book_rental.models.language import BookLanguage
from ecommerce.models.sales.product import Product
from generics.libs.reader.excel_file_reader import ExcelFileReader


class Book(Product):
    isbn = models.CharField(max_length=500, blank=True)  # The 10 digit ISBN code
    isbn13 = models.CharField(max_length=500, blank=True)
    edition = models.CharField(max_length=100)
    publisher = models.ForeignKey(BookPublisher, null=True)
    authors = models.ManyToManyField(Author)
    publish_date = models.DateField(null=True)
    language = models.ForeignKey(BookLanguage)
    page_count = models.IntegerField(default=0)

    @classmethod
    def get_table_headers(self):
        return [
            "ID", "Code", "Title", "Title2", "Active?", "Show 2", "Details"
        ]

    @classmethod
    def prepare_table_data(self, queryset):
        data = []
        for q_object in queryset:
            data += [
                [
                    q_object.pk, q_object.code, q_object.title, q_object.title_2, "Yes" if q_object.is_active else "No",
                    "Yes" if q_object.show_2 else "No",
                    '<a href="%s">Details</a>' % q_object.get_detail_link(object_id=q_object.pk)
                ]
            ]
        return data

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

    @classmethod
    def get_download_headers(cls):
        return ["Code", "Book Title", "Book Subtitle", "ISBN", "Description", "Category Code(s)", "Edition",
            "Total Page", "Publisher Code", "Published date(dd/mm/YYYY)", "Cover Photo", "Language", "Keyword(s)"]

    @classmethod
    def get_download_template_headers(cls):
        return []

    @classmethod
    def prepare_download_template_data(cls, queryset):
        template_data = []
        for q_object in queryset:
            template_data += [
                [q_object.code, q_object.name, q_object.name_2, q_object.description, q_object.description_2,
                 "1" if q_object.show_2 else "0", q_object.image.name if q_object.image else '',
                 q_object.get_emails(), q_object.get_phones()]]
        return template_data

    @classmethod
    def get_downloader_class(cls):
        return BookDownloader

    @classmethod
    def get_download_file_name(cls):
        return "Book List"

    @classmethod
    def get_reader_class(cls):
        return ExcelFileReader

    @classmethod
    def get_uploader_class(cls):
        return BookUploader

    @classmethod
    def get_download_link(cls):
        return reverse("admin_book_download_view")

    @classmethod
    def get_upload_link(cls):
        return reverse("admin_book_upload_view")

    @classmethod
    def get_activate_link(cls):
        return reverse("admin_book_activate_view")

    @classmethod
    def get_deactivate_link(cls):
        return reverse("admin_book_deactivate_view")

    @classmethod
    def get_delete_link(cls):
        return reverse("admin_book_delete_view")

    @classmethod
    def get_detail_link(cls, object_id):
        return ""

    @classmethod
    def get_create_link(cls):
        return reverse("admin_book_create_view")

    @classmethod
    def get_edit_link_name(cls):
        return ""

    @classmethod
    def get_edit_link(cls, object_id):
        return ""

    @classmethod
    def get_search_by_options(cls):
        options = super(Book, cls).get_search_by_options()
        options += [
            ("By Title", "title"),
            ("By Description", "description"),
            ("By Keywords", "keyword"),
            ("By ISBN", "isbn"),
            ("By Edition", "edition"),
            ("By Author", "author"),
            ("By Publisher", "publisher"),
            ("By Category", "category"),
            ("By Sale Available", "sale_available"),
            ("By Rent Available", "rent_available")
        ]
        return options

    @classmethod
    def apply_search_filters(cls, request, queryset=None):
        queryset = super(Book, cls).apply_search_filters(request, queryset=queryset)
        if not queryset:
            queryset = cls.objects.all()
        by = request.GET.get("by", None)
        keyword = request.GET.get('keyword', None)
        # if by and keyword:
        #     if by == "name":
        #         queryset = queryset.filter(Q(name__icontains=keyword) | Q(name_2__icontains=keyword))
        return queryset