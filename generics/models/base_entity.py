import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from book_rental.libs.downloader.downloader import Downloader
from book_rental.libs.uploader.uploader import Uploader
from bradmin.enums import ViewAction
from engine.clock.Clock import Clock
from generics.manager.modelmanager.base_entity_model_manager import BaseEntityModelManager
from generics.mixin.modelmixin.filter_model_mixin import FilterModelMixin
from generics.mixin.modelmixin.permission_model_mixin import PermissionModelMixin
from generics.mixin.modelmixin.searchable_model_mixin import SearchableModelMixin
from generics.mixin.modelmixin.template_provider_mixin import TemplateProviderMixin
from generics.models.code_pointer import CodePointer


class BaseEntity(PermissionModelMixin, FilterModelMixin, TemplateProviderMixin,
                 SearchableModelMixin, models.Model):
    code = models.CharField(max_length=50)
    date_created = models.BigIntegerField()
    last_updated = models.BigIntegerField()
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    last_updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)

    objects = BaseEntityModelManager(filter=settings.GLOBAL_MODEL_FILTER)

    def __str__(self):
        return self.code

    @classmethod
    def get_view_actions(cls):
        return {
            ViewAction.CREATE: "",
            ViewAction.EDIT: "",
            ViewAction.EDIT_NAME: "",
            ViewAction.DELETE: "",
            ViewAction.UPLOAD: "",
            ViewAction.DOWNLOAD: "",
            ViewAction.DOWNLOAD_TEMPLATE: "",
            ViewAction.ACTIVATE: "",
            ViewAction.DEACTIVATE: "",
            ViewAction.APPROVE: "",
            ViewAction.REJECT: ""
        }

    @classmethod
    def show_upload(cls):
        return False
        
    @classmethod
    def show_upload_as(cls):
        return "Upload"

    @classmethod
    def show_download(cls):
        return False
        
    @classmethod
    def show_download_as(cls):
        return "Download"

    @classmethod
    def show_download_template(cls):
        return False
        
    @classmethod
    def show_download_template_as(cls):
        return "Download Template"

    @classmethod
    def show_create(cls):
        return False
        
    @classmethod
    def show_create_as(cls):
        return "Create"

    @classmethod
    def show_edit(cls):
        return False
        
    @classmethod
    def show_edit_as(cls):
        return "Edit"

    @classmethod
    def show_delete(cls):
        return False
        
    @classmethod
    def show_delete_as(cls):
        return "Delete"

    @classmethod
    def show_activate(cls):
        return False
        
    @classmethod
    def show_activate_as(cls):
        return "Activate"

    @classmethod
    def show_deactivate(cls):
        return False
        
    @classmethod
    def show_deactivate_as(cls):
        return "Deactivate"

    @classmethod
    def show_approve(cls):
        return False
        
    @classmethod
    def show_approve_as(cls):
        return "Approve"

    @classmethod
    def show_reject(cls):
        return False
        
    @classmethod
    def show_reject_as(cls):
        return "Reject"

    def get_code_prefix(self):
        prefix = ''.join([c for c in self.__class__.__name__ if c.isupper()])
        return prefix if prefix else self.__class__.__name__

    @classmethod
    def approve(cls, id_list=[]):
        pass

    @classmethod
    def reject(cls, id_list=[]):
        pass

    @classmethod
    def activate(cls, id_list=[]):
        object_list = cls.objects.filter(pk__in=id_list)
        object_list.update(is_active=True)

    @classmethod
    def deactivate(cls, id_list=[]):
        object_list = cls.objects.filter(pk__in=id_list)
        object_list.update(is_active=False)

    @classmethod
    def soft_delete(cls, id_list=[]):
        object_list = cls.objects.filter(pk__in=id_list)
        object_list.update(is_deleted=True)

    @classmethod
    def get_table_headers(self):
        return []

    @classmethod
    def prepare_table_data(cls, queryset):
        return []

    @classmethod
    def prepare_download_template_data(cls, queryset):
        return []

    @classmethod
    def get_download_headers(cls):
        return [
            "Code", "Name"
        ]

    @classmethod
    def get_download_template_headers(cls):
        return [
            "Code", "Name"
        ]

    @classmethod
    def get_downloader_class(cls):
        return Downloader

    @classmethod
    def get_uploader_class(cls):
        return Uploader

    @classmethod
    def get_download_file_name(cls):
        return str(uuid.uuid4())

    @classmethod
    def get_writter_class(cls):
        return None

    @classmethod
    def get_reader_class(cls):
        return None

    @classmethod
    def prepare_download_data(cls, queryset):
        return []

    @classmethod
    def get_advanced_search_options(cls):
        return [
            ("Is Active", "is_active")
        ]

    @classmethod
    def get_search_by_options(cls):
        return [
            ("By ID", "id"),
            ("By Code", "code")
        ]

    @classmethod
    def get_datefields(cls):
        return []

    @classmethod
    def apply_search_filters(cls, request, queryset=None):
        if not queryset:
            queryset = cls.objects.all()
        id = request.GET.get("id", None)
        code = request.GET.get("code", None)
        if id:
            try:
                id = int(id)
                queryset = queryset.filter(pk=id)
            except:
                queryset = cls.objects.none()
        if code:
            queryset = queryset.filter(code=code)
        return queryset

    @classmethod
    def get_detail_link(cls, object_id):
        return ""

    def get_object_detail_link(self):
        return ""

    @classmethod
    def get_create_link(cls):
        return ""

    @classmethod
    def get_edit_link_name(cls):
        return ""

    @classmethod
    def get_edit_link(cls, object_id):
        return ""

    @classmethod
    def get_activate_link(cls):
        return ""

    @classmethod
    def get_deactivate_link(cls):
        return ""

    @classmethod
    def get_list_url(cls):
        return ""

    @classmethod
    def get_download_link(cls):
        return ""

    @classmethod
    def get_upload_link(cls):
        return ""

    @classmethod
    def get_delete_link(cls):
        return ""

    @classmethod
    def get_approve_link(cls):
        return ""

    @classmethod
    def get_reject_link(cls):
        return ""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not self.pk:
            self.date_created = Clock.utc_timestamp()

            last_code_objects = CodePointer.objects.filter(model_name=self.__class__.__name__)
            if not last_code_objects.exists():
                last_code_object = CodePointer()
                last_code_object.model_name = self.__class__.__name__
                last_code_object.value = 1
                last_code_object.save()
            else:
                last_code_object = last_code_objects.first()
                last_code_object.model_name = self.__class__.__name__
                last_code_object.value += 1
                last_code_object.save()

            self.code = self.get_code_prefix() + "-" + str(format(last_code_object.value, '06d'))

        self.last_updated = Clock.utc_timestamp()
        super(BaseEntity, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True
