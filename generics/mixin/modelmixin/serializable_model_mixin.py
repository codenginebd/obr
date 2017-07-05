from collections import OrderedDict
import uuid
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.db.models.manager import Manager
from rest_framework import serializers
from django.db import transaction


class SerializableModelMixin(object):
    @classmethod
    def get_serializer(cls):
        class BESerializer(serializers.ModelSerializer):

            def __init__(self, *args, fields=None, context=None, **kwargs):
                super(SerializableModelMixin, self).__init__(*args, context=context, **kwargs)

                if bool(context):
                    fields = context['request'].QUERY_PARAMS.get('fields', None)
                    if bool(fields):
                        if isinstance(fields, tuple) or isinstance(fields, list):
                            pass
                        else:
                            fields = (fields,)

                        allowed = set(fields)
                        existing = set(self.fields.keys())
                        for field_name in existing - allowed:
                            self.fields.pop(field_name)

            def update(self, instance, validated_data):
                with transaction.atomic():
                    instance.last_updated_by = self.context['request'].user

                    m2m_fields = self.Meta.model._meta.get_m2m_with_model()
                    m2m_dict = dict()
                    for m in m2m_fields:
                        m2m_dict[m[0].name] = validated_data.pop(m[0].name, [])

                    attributes = self.Meta.model._meta.fields

                    for attr in attributes:
                        if attr.name in validated_data and isinstance(validated_data[attr.name], dict):
                            _obj = getattr(instance, attr.name)
                            if attr.name in [x[0] for x in self.Meta.model.get_custom_serializers()]:
                                _serializer = \
                                list(filter(lambda a: a[0] == attr.name, self.Meta.model.get_custom_serializers()))[0][
                                    1](context=self.context)
                            else:
                                _serializer = attr.related.parent_model.get_serializer()(context=self.context)

                            if _obj is None:
                                validated_data[attr.name] = _serializer.create(validated_data[attr.name])
                            else:
                                validated_data[attr.name] = _serializer.update(_obj, validated_data[attr.name])

                    for attr in attributes:
                        if attr.name in validated_data.keys():
                            if isinstance(attr, ForeignKey) or isinstance(attr, OneToOneField):
                                # _obj = getattr(instance, attr.name)
                                value = validated_data.pop(attr.name, None)
                                if isinstance(value, Model) and value.pk is None:
                                    value.save()
                                setattr(instance, attr.name,
                                        attr.model.objects.get(pk=value) if isinstance(value, int) else value)

                    for m in m2m_fields:
                        if m[0].name in m2m_dict.keys() and len(m2m_dict[m[0].name]) > 0:
                            _field = getattr(instance, m[0].name)
                            _values = m2m_dict[m[0].name]
                            if m[0].name in instance.__class__.get_dependent_field_list():
                                if isinstance(_values, User):
                                    _values.delete()
                                elif isinstance(_values, Model):
                                    temp = _values
                                    setattr(instance, m[0].name, None)
                                    instance.save()
                                    temp.delete(force_delete=True)
                                elif isinstance(_values, Manager):
                                    items = list(_values.all())
                                    _values.clear()
                                    for item in items:
                                        item.delete(force_delete=True)
                                else:
                                    pass

                            if m[0].name in [x for x in instance.__class__.get_dependent_field_list() if
                                             isinstance(getattr(instance, x), Manager)]:
                                _field.clear()
                            for v in _values:
                                if isinstance(v, (dict, OrderedDict)):
                                    if m[0].name in [x[0] for x in self.Meta.model.get_custom_serializers()]:
                                        _serializer = list(filter(lambda a: a[0] == m[0].name,
                                                                  self.Meta.model.get_custom_serializers()))[0][1](
                                            context=self.context)
                                    else:
                                        _serializer = m[0].related.parent_model.get_serializer()(context=self.context)
                                    if isinstance(v, int):
                                        v = m[0].related.parent_model.objects.get(pk=v)
                                    else:
                                        v = _serializer.create(v)

                                if m[0].name in [x[0] for x in self.Meta.model.intermediate_models()]:
                                    i_field = \
                                    list(filter(lambda x: x[0] == m[0].name, self.Meta.model.intermediate_models()))[0]
                                    setattr(v, i_field[3], instance)
                                    v.save()
                                else:
                                    v.save()
                                    _field.add(v)

                    return super().update(instance, validated_data)

            def save(self, **kwargs):
                return super().save(**kwargs)

            def create(self, validated_data):
                with transaction.atomic():
                    id = validated_data.pop('id')
                    responseObj = self.Meta.model.objects.filter(pk=id)
                    if responseObj.exists():
                        return responseObj.first()

                    validated_data.update({
                        "created_by": self.context['request'].user,
                        "last_updated_by": self.context['request'].user,
                        "id": id
                    })
                    m2m_fields = self.Meta.model._meta.get_m2m_with_model()
                    m2m_dict = dict()
                    for m in m2m_fields:
                        m2m_dict[m[0].name] = validated_data.pop(m[0].name, [])

                    attributes = self.Meta.model._meta.fields

                    for attr in attributes:
                        if attr.name in validated_data and isinstance(validated_data[attr.name], dict):
                            _serializer = attr.related.parent_model.get_serializer()(context=self.context)
                            validated_data[attr.name] = _serializer.create(validated_data[attr.name])

                    pk = validated_data.pop('id', None)
                    if pk:
                        obj = self.Meta.model.objects.get(pk=pk)
                    else:
                        obj = self.Meta.model.objects.create(**validated_data)

                    for attr in attributes:
                        if isinstance(attr, ForeignKey) or isinstance(attr, OneToOneField):
                            value = validated_data.pop(attr.name, None)
                            if isinstance(value, Model) and value.pk is None:
                                value.save()
                            setattr(obj, attr.name,
                                    attr.model.objects.get(pk=value) if isinstance(value, int) else value)
                        else:
                            pass
                    obj.save()

                    for m in m2m_fields:
                        _field = getattr(obj, m[0].name)
                        _values = m2m_dict[m[0].name]
                        for v in _values:
                            if isinstance(v, (dict, OrderedDict)):
                                if m[0].name in [x[0] for x in self.Meta.model.get_custom_serializers()]:
                                    _serializer = \
                                    list(filter(lambda a: a[0] == m[0].name, self.Meta.model.get_custom_serializers()))[
                                        0][1](context=self.context)
                                else:
                                    _serializer = m[0].related.parent_model.get_serializer()(context=self.context)
                                v = _serializer.create(v)

                            if m[0].name in [x[0] for x in self.Meta.model.intermediate_models()]:
                                i_field = \
                                list(filter(lambda x: x[0] == m[0].name, self.Meta.model.intermediate_models()))[0]
                                setattr(v, i_field[3], obj)
                                v.save()
                            else:
                                v.save()
                                _field.add(v)

                    return obj

            def mutate(self, **kwargs):
                self.instance = self.instance.mutate_to()
                return self.instance

            def approve(self, **kwargs):
                self.instance = self.instance.approve_to(**kwargs)
                return self.instance

            def reject(self, **kwargs):
                self.instance = self.instance.reject_to(**kwargs)
                return self.instance

            class Meta:
                model = cls
                read_only_fields = (
                'created_by', 'code', 'type', 'id', 'last_updated', 'date_created', 'last_updated_by',
                'is_active', 'is_deleted', 'is_locked', 'timestamp')

        return BESerializer