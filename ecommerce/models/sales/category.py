from django.db import models
from django.db.models.query_utils import Q
from django.template.defaultfilters import slugify
from django.urls.base import reverse
from book_rental.libs.downloader.category_downloader import CategoryDownloader
from book_rental.libs.uploader.category_uploader import CategoryUploader
from generics.libs.reader.excel_file_reader import ExcelFileReader
from generics.models.base_entity import BaseEntity


class ProductCategory(BaseEntity):
    name = models.CharField(max_length=500)
    name_2 = models.CharField(max_length=500)
    show_name_2 = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)

    @classmethod
    def get_all_parent_categories(cls, **kwargs):
        return cls.objects.filter(parent__isnull=True)

    @classmethod
    def get_all_descendants(cls, cat_id=None, **kwargs):
        pass

    @classmethod
    def get_download_link(cls):
        return reverse("admin_category_download_view")
        
    @classmethod
    def get_all_children(cls, cat_id=None, **kwargs):
        all_categories = []
        
        if not cat_id:
            # For All Categories
            # Get All categories whose parent is None
            all_parent_categories = ProductCategory.objects.filter(parent__isnull=True)
            for parent_cat in all_parent_categories:
                direct_childs = ProductCategory.objects.filter(parent_id=parent_cat.pk)
                all_categories += [
                    {
                        "id": parent_cat.pk,
                        "name": parent_cat.name,
                        "name_2": parent_cat.name_2,
                        "show_name_2": parent_cat.show_name_2,
                        "slug": parent_cat.slug,
                        "instance": parent_cat,
                        "children": direct_childs
                    }
                ]
        else:
            parent_cat = ProductCategory.objects.get(pk=cat_id)
            direct_childs = ProductCategory.objects.filter(parent_id=cat_id)
            all_categories = {
                    "id": parent_cat.pk,
                    "name": parent_cat.name,
                    "name_2": parent_cat.name_2,
                    "show_name_2": parent_cat.show_name_2,
                    "slug": parent_cat.slug,
                    "instance": parent_cat,
                    "children": direct_childs
                }
            
        return all_categories

    @classmethod
    def get_download_headers(cls):
        return ["Code", "Name(English)", "Name(Bangla)", "Show Bangla", "Parent"]

    @classmethod
    def get_download_template_headers(cls):
        return ["Code", "Name(English)", "Name(Bangla)", "Show Bangla", "Parent"]

    @classmethod
    def prepare_table_data(cls, queryset):
        table_data = []
        for q_object in queryset:
            table_data += [[q_object.code, q_object.name, q_object.name_2,
                            "Yes" if q_object.show_name_2 else "No", q_object.parent.name if q_object.parent else "-"]]
        return table_data

    @classmethod
    def prepare_download_template_data(cls, queryset):
        template_data = []
        for q_object in queryset:
            template_data += [[q_object.code, q_object.name, q_object.name_2,
                            "1" if q_object.show_name_2 else "0", q_object.parent.name if q_object.parent else ""]]
        return template_data

    @classmethod
    def get_downloader_class(cls):
        return CategoryDownloader

    @classmethod
    def get_download_file_name(cls):
        return "Catgeory List"

    @classmethod
    def get_reader_class(cls):
        return ExcelFileReader

    @classmethod
    def get_uploader_class(cls):
        return CategoryUploader

    @classmethod
    def get_upload_link(cls):
        return reverse("admin_category_upload_view")

    @classmethod
    def get_activate_link(cls):
        return reverse("admin_category_activate_view")

    @classmethod
    def get_deactivate_link(cls):
        return reverse("admin_category_deactivate_view")

    @classmethod
    def get_delete_link(cls):
        return reverse("admin_category_delete_view")

    @classmethod
    def get_create_link(cls):
        return reverse("admin_category_create_view")

    @classmethod
    def get_edit_link_name(cls):
        return "admin_category_edit_link_view"

    @classmethod
    def get_edit_link(cls, object_id):
        return reverse("admin_category_edit_link_view", kwargs={"pk": object_id})

    @classmethod
    def get_list_url(cls):
        return reverse("admin_category_view")

    @classmethod
    def get_detail_link(cls, object_id):
        return reverse("admin_category_details_view", kwargs={'pk': object_id})

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
    def apply_search_filters(cls, request, queryset=None):
        queryset = super(ProductCategory, cls).apply_search_filters(request, queryset=queryset)
        if not queryset:
            queryset = cls.objects.all()
        by = request.GET.get("by", None)
        keyword = request.GET.get('keyword', None)
        if by and keyword:
            if by == "name":
                queryset = queryset.filter(Q(name__icontains=keyword) | Q(name_2__icontains=keyword))
        return queryset

    @classmethod
    def get_search_by_options(cls):
        return [
            ("By ID", "id"),
            ("By Code", "code"),
            ("By Name", "name")
        ]

    @classmethod
    def get_datefields(cls):
        return ["name"]

        
        

