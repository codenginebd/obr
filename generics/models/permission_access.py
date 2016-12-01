from django.db import models
from generics.models.base_entity import BaseEntity
from generics.models.permission import BRPermission
from generics.models.role import BRole


class BRPermissionAccess(BaseEntity):
    role = models.ForeignKey(BRole)
    permission = models.ForeignKey(BRPermission)
    object_type = models.CharField(max_length=200)
    object_id = models.CharField(max_length=200)