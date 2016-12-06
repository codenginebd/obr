from django.contrib.auth.models import User
from django.db import models
from django.db.models.query_utils import Q
from engine.clock.Clock import Clock
from generics.middleware.br_middleware import BRRequestMiddleware
from generics.mixin.modelmixin.filter_model_mixin import FilterModelMixin
from generics.mixin.modelmixin.permission_model_mixin import PermissionModelMixin
from generics.mixin.modelmixin.searchable_model_mixin import SearchableModelMixin
from generics.mixin.modelmixin.template_provider_mixin import TemplateProviderMixin
from generics.models.code_pointer import CodePointer


class BaseEntityModelManager(models.Manager):
    _filter = None

    def __init__(self, *args, filter=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._filter = filter
        self.kwargs = kwargs

    def get_queryset(self):
        if self._filter is not None:
            return super().get_queryset().filter(Q(**self._filter))

        current_request = BRRequestMiddleware.get_request()

        queryset = super().get_queryset()
        queryset = self.model.apply_permissions(queryset, request=current_request, **(self.kwargs))
        queryset = self.model.apply_filter(queryset, request=current_request, **(self.kwargs))
        queryset = self.model.apply_search(queryset, request=current_request, **(self.kwargs))
        return queryset


class BaseEntity(models.Model, PermissionModelMixin, FilterModelMixin, TemplateProviderMixin,
                 SearchableModelMixin):
    code = models.CharField(max_length=50)
    date_created = models.BigIntegerField()
    last_updated = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='+', null=True)
    last_updated_by = models.ForeignKey(User, related_name='+', null=True)

    objects = BaseEntityModelManager()

    def get_code_prefix(self):
        prefix = ''.join([c for c in self.__class__.__name__ if c.isupper()])
        return prefix if prefix else self.__class__.__name__

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