from django.contrib.auth.models import User
from django.db import models
from engine.clock.Clock import Clock
from generics.manager.modelmanager.base_entity_model_manager import BaseEntityModelManager
from generics.mixin.modelmixin.filter_model_mixin import FilterModelMixin
from generics.mixin.modelmixin.permission_model_mixin import PermissionModelMixin
from generics.mixin.modelmixin.searchable_model_mixin import SearchableModelMixin
from generics.mixin.modelmixin.template_provider_mixin import TemplateProviderMixin
from generics.models.code_pointer import CodePointer


class BaseEntity(models.Model, PermissionModelMixin, FilterModelMixin, TemplateProviderMixin,
                 SearchableModelMixin):
    code = models.CharField(max_length=50)
    date_created = models.BigIntegerField()
    last_updated = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='+', null=True)
    last_updated_by = models.ForeignKey(User, related_name='+', null=True)

    objects = BaseEntityModelManager()

    def get_code_prefix(self):
        prefix = ''.join([c for c in self.__class__.__name__ if c.isupper()])
        return prefix if prefix else self.__class__.__name__

    @classmethod
    def get_detail_link(cls, object_id):
        return ""

    @classmethod
    def get_edit_link(cls, object_id):
        return ""

    @classmethod
    def get_activate_link(cls, object_id):
        return ""

    @classmethod
    def get_deactivate_link(cls, object_id):
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
