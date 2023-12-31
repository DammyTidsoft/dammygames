import uuid

from django.db import models
from django.db.models import Q
from jsonfield import JSONField

from api.queryset import ActiveQuerySet
from users.models import User


# Create your models here.


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = ActiveQuerySet.as_manager()

    class Meta:
        abstract = True


class Entity(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    owners = models.ManyToManyField(User, related_name="entities", blank=True)

    class Meta:
        verbose_name_plural = "Offices"
        verbose_name = "Office"

    def __str__(self):
        return self.name

    def _hasattr(self, attr_slug):
        return attr_slug in self.__dict__

    def get_all_attributes(self):
        return list(self.attributes.values_list("slug", flat=True).distinct())

    def filter(self, **kwargs):
        attributes = self.attributes.all()
        attributes_dict = {attr.slug: attr for attr in attributes}
        q = Q()
        for key, value in kwargs.items():
            if key in attributes_dict:
                attr = attributes_dict[key]
                q |= Q(**{"value_%s" % attr.data_type: value, "attribute_id": attr.id})

            else:
                q &= Q(**{key: value})
        qs = self.values.filter(q)
        # Get related values
        return self.values.filter(uuid__in=qs.values_list("uuid", flat=True))

    def exclude(self, **kwargs):
        attributes = self.attributes.all()
        attributes_dict = {attr.slug: attr for attr in attributes}
        q = Q()
        for key, value in kwargs.items():
            if key in attributes_dict:
                attr = attributes_dict[key]
                q |= Q(**{"value_%s" % attr.data_type: value, "attribute_id": attr.id})

            else:
                q &= Q(**{key: value})
        qs = self.values.exclude(q)
        # Get related values
        return self.values.filter(uuid__in=qs.values_list("uuid", flat=True))

    def create(self, **kwargs):
        values = []
        attributes = self.attributes.all()
        attributes_dict = {attr.slug: attr for attr in attributes}
        attr_uuid = uuid.uuid4()
        data = {}

        # Get all the attributes that are passed in kwargs
        for key in list(kwargs):
            if key in attributes_dict:
                attr = attributes_dict[key]
                data[attr.id] = kwargs[key]
                kwargs.pop(key)

        # Create values for all the attributes
        for key, val in data.items():
            value = Value(attribute_id=key, entity=self, uuid=attr_uuid, value=val)
            for k, v in kwargs.items():
                setattr(value, k, v)
            values.append(value)
        return Value.objects.bulk_create(values)

    def process_values(self, values):
        data = {}
        for value in values:
            attr = value.attribute
            if attr.slug not in data:
                data[attr.slug] = value.value
        return data

    def filter_values(self, **kwargs):
        return self.process_values(self.filter(**kwargs))

    def exclude_values(self, **kwargs):
        return self.process_values(self.exclude(**kwargs))


class Attribute(AbstractBaseModel):
    DATA_TYPES = (
        ("str", "String"),
        ("int", "Integer"),
        ("float", "Float"),
        ("bool", "Boolean"),
        ("date", "Date"),
        ("datetime", "DateTime"),
        ("time", "Time"),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="attributes"
    )
    point = models.IntegerField(default=0)
    data_type = models.CharField(max_length=255, choices=DATA_TYPES, default="str")

    required = models.BooleanField(default=False)

    class Meta:
        unique_together = ("entity", "slug")
        verbose_name_plural = "Questions"
        verbose_name = "Question"

    def __str__(self):
        return self.name

    def save_value(self, value, **kwargs):
        value_obj = Value(attribute=self, entity=self.entity, **kwargs)
        value_type = "value_{}".format(self.data_type)
        setattr(value_obj, value_type, value)
        value.save()


class Value(AbstractBaseModel):
    SUBMISSION_TYPES = (
        ("dila", "Dila"),
        ("muqami", "Muqami"),
        ("state", "State"),
    )
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="values"
    )
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="values")
    uuid = models.UUIDField(
        null=True, blank=True
    )  # used for connecting values across attributes

    submitted_by = models.CharField(max_length=20, blank=False)
    submitted_for = models.CharField(
        max_length=255, blank=False, null=True
    )  # dilaId, MuqamiId, StateId
    submission_type = models.CharField(
        max_length=20, blank=False, null=True, choices=SUBMISSION_TYPES
    )  # dila, muqami, state

    month = models.IntegerField(null=True, blank=False)
    year = models.IntegerField(null=True, blank=False)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="values"
    )

    value_str = models.TextField(null=True, blank=True)
    value_int = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_bool = models.BooleanField(null=True, blank=True)
    value_date = models.DateTimeField(null=True, blank=True)
    value_datetime = models.DateTimeField(null=True, blank=True)
    value_time = models.TimeField(null=True, blank=True)
    value_json = JSONField(default=dict, null=True, blank=True)
    value_file = models.FileField(null=True, blank=True)

    @classmethod
    def extra_fields(cls):
        hidden_fields = [
            "value_json",
            "value_str",
            "value_int",
            "value_float",
            "value_file",
            "value_bool",
            "value_date",
            "value_datetime",
            "value_time",
            "id",
            "active",
            "attribute",
            "entity",
        ]
        return [
            field.name
            for field in cls._meta.get_fields()
            if field.name not in hidden_fields
        ]

    def __str__(self):
        return "{}: {}".format(self.attribute.name, self.value)

    def _get_value(self):
        value_type = "value_{}".format(self.attribute.data_type)
        return getattr(self, value_type)

    def _set_value(self, value):
        value_type = "value_{}".format(self.attribute.data_type)
        setattr(self, value_type, value)

    value = property(_get_value, _set_value)
