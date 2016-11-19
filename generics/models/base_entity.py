from django.contrib.auth.models import User
from django.db import models
from engine.clock.Clock import Clock


class BaseEntity(models.Model):
    code = models.CharField(max_length=50)
    date_created = models.BigIntegerField()
    last_updated = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, related_name='+', null=True)
    last_updated_by = models.ForeignKey(User, related_name='+', null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not self.pk:
            self.date_created = Clock.utc_timestamp()
        self.date_modified = Clock.utc_timestamp()
        super(BaseEntity, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True