from django.db import models
from django.urls.base import reverse

from generics.models.base_entity import BaseEntity


class FrontPalette(BaseEntity):
    name = models.CharField(max_length=500)
    name_2 = models.CharField(max_length=500, blank=True)
    show_2 = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

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
        return reverse("admin_front_palette_create_view")

    @classmethod
    def get_edit_link(cls, object_id):
        return reverse("admin_front_palette_edit_link_view", kwargs={"pk": object_id})

    @classmethod
    def get_edit_link_name(cls):
        return "admin_front_palette_edit_link_view"

    @classmethod
    def get_activate_link(cls):
        return reverse("admin_front_palette_activate_view")

    @classmethod
    def get_deactivate_link(cls):
        return reverse("admin_front_palette_deactivate_view")

    @classmethod
    def get_delete_link(cls):
        return reverse("admin_front_palette_delete_view")

    @classmethod
    def get_table_headers(self):
        return ["ID", "Code", "Name", "Name 2", "Show 2", "Is Active", "Palette Order"]

    @classmethod
    def prepare_table_data(cls, queryset):
        data = []
        for q_object in queryset:
            data += [
                [q_object.pk, q_object.code,
                 q_object.name, q_object.name_2, "Yes" if q_object.show_2 else "No",
                 "Yes" if q_object.is_active else "No", q_object.order]
            ]
        return data