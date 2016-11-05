from django.db import models
from django.auth.models import User

class BaseEntity(models.Model):
    code = models.CharField(max_length=50)
    date_created = models.BigIntegerField()
    last_updated = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, null=True)
    lasst_updated_by = models.ForeignKey(User, null=True)

    class Meta:
        abstract = True