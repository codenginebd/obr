from generics.manager.modelmanager.base_entity_model_manager import BaseEntityModelManager
from generics.models.location_entity import LocationEntity


class Country(LocationEntity):
    objects = BaseEntityModelManager(filter={'type': 'Country'})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.type = self.__class__.__name__
        super(Country, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        proxy = True

    def __str__(self):
        return self.code + ": " + self.short_name + "(%s)" % self.name
