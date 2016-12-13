from generics.manager.modelmanager.base_entity_model_manager import BaseEntityModelManager
from generics.models.location_entity import LocationEntity


class District(LocationEntity):

    objects = BaseEntityModelManager(filter={'type': 'District'})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.type = self.__class__.__name__
        super(District, self).save(force_insert=force_insert, force_update=force_update,
                                  using=using, update_fields=update_fields)

    class Meta:
        proxy = True