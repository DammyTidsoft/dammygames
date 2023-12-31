from rest_framework import serializers

from api.models import Entity, Value, Attribute


class AttributeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    slug = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    data_type = serializers.CharField(max_length=200)
    required = serializers.BooleanField()
    active = serializers.BooleanField()

    @staticmethod
    def validate_date_type(value):
        if value not in Attribute.DATA_TYPES:
            raise serializers.ValidationError("Invalid data type")
        return value

    def create(self, validated_data):
        return Attribute.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.description = validated_data.get("description", instance.description)
        instance.data_type = validated_data.get("data_type", instance.data_type)
        instance.required = validated_data.get("required", instance.required)
        instance.active = validated_data.get("active", instance.active)
        instance.save()
        return instance


class EntitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    slug = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    attributes = serializers.ListSerializer(child=AttributeSerializer())

    def to_representation(self, instance):
        data = super(EntitySerializer, self).to_representation(instance)
        data["attributes"] = AttributeSerializer(
            instance.attributes.active(), many=True
        ).data
        return data

    @staticmethod
    def validate_slug(value):
        if Entity.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Entity with this slug already exists")
        return value

    def create(self, validated_data):
        attributes = validated_data.pop("attributes")
        entity = Entity.objects.create(**validated_data)
        for attribute in attributes:
            Attribute.objects.create(entity=entity, **attribute)

        return entity

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance


class ValueSerializer:
    def __init__(self, entity, data=None, values=None):
        if data is None:
            data = {}
        if values is None:
            values = []

        self.data = data
        self.initial_data = data
        self.values = values
        self.entity = entity
        self.errors = []
        self.validated_data = {}

    def serialize(self):
        for value in self.values:
            attr = value.attribute
            if attr.active:
                self.data[value.attribute.slug] = value.value
        # Pick one value and get the remaining fields
        if self.values:
            value = self.values[0]
            for field in [field.name for field in Value.extra_fields()]:
                if field not in self.data:
                    self.data[field] = getattr(value, field)
        return self.data

    def sanitize(self):
        attributes = self.entity.attributes.all()
        attributes_dict = {attr.slug: attr for attr in attributes}
        value_fields = [field.name for field in Value.extra_fields()]
        for key, value in self.data.items():
            if key in attributes_dict:
                attr = attributes_dict[key]
                self.validated_data[attr.slug] = value
            elif key in value_fields:
                self.validated_data[key] = value
            else:
                self.errors.append("Invalid attribute: %s" % key)

        # Check for required attributes
        # for attr in attributes:
        #     if attr.required and not attr.slug not in self.validated_data:
        #         self.errors.append('%s is required' % attr.slug)

        # TODO Check for data types

    def validate(self):
        self.sanitize()
        return self.errors

    def save(self):
        errors = self.validate()
        if errors:
            return errors
        self.values = self.entity.create(**self.validated_data)
        return self.serialize()
