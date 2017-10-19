from django.conf import settings
from django.urls.base import reverse

from generics.libs.utils import merge_dict
from generics.manager.modelmanager.base_entity_model_manager import BaseEntityModelManager
from generics.models.location_entity import LocationEntity


class Country(LocationEntity):
    objects = BaseEntityModelManager(filter=merge_dict(settings.GLOBAL_MODEL_FILTER, {'type': 'Country'}))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.type = self.__class__.__name__
        super(Country, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        proxy = True

    def __str__(self):
        return self.code + ": " + self.short_name + "(%s)" % self.name

    @classmethod
    def show_create(cls):
        return True

    @classmethod
    def show_edit(cls):
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
        return reverse("admin_country_create_view")

    @classmethod
    def get_edit_link(cls, object_id):
        return reverse("admin_country_edit_link_view", kwargs={"pk": object_id})

    @classmethod
    def get_edit_link_name(cls):
        return "admin_country_edit_link_view"

    @classmethod
    def get_activate_link(cls):
        return reverse("admin_country_activate_view")

    @classmethod
    def get_deactivate_link(cls):
        return reverse("admin_country_deactivate_view")

    @classmethod
    def get_delete_link(cls):
        return reverse("admin_country_delete_view")

    @classmethod
    def get_table_headers(self):
        return ["ID", "Code", "Name", "Short Name", "Is Active"]

    @classmethod
    def prepare_table_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [q_object.pk, q_object.code, q_object.name, q_object.short_name,
                 "Yes" if q_object.is_active else "No"]
            ]
        return data
