from django.test import TestCase

from api.models import Entity, Attribute


class TestEntity(TestCase):
    def setUp(self):
        self.entity = Entity.objects.create(name="test entity")

    def test_entity_created(self):
        self.assertEqual(self.entity.name, "test entity")

    def test_entity_str(self):
        self.assertEqual(str(self.entity), "test entity")

    def test_entity_get_all_attributes(self):
        self.assertEqual(self.entity.get_all_attributes(), [])


class TestAttribute(TestCase):
    @classmethod
    def setUpTestData(cls):
        entity = Entity.objects.create(name="test entity")
        cls.attribute = Attribute.objects.create(
            name="test attribute", entity=entity, description="test description"
        )

    def test_attribute_created(self):
        self.assertEqual(self.attribute.name, "test attribute")

    def test_attribute_str(self):
        self.assertEqual(str(self.attribute), "test attribute")
