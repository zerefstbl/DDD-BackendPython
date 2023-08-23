import unittest

from dataclasses import dataclass, is_dataclass

from __seedwork.domain.entities import Entity
from __seedwork.domain.value_objects import UniqueEntityId

from abc import ABC


@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
    prop1: str
    prop2: str


class TestEntityUnit(unittest.TestCase):
    
    def test_if_is_dataclass(self):
        self.assertTrue(is_dataclass(Entity))
        
    def test_if_is_abstract_class(self):
        self.assertIsInstance(Entity(), ABC)

    def test_set_id_and_props(self):
        entity = StubEntity(prop1="value1", prop2="value2")
        self.assertEqual(entity.prop1, "value1")
        self.assertEqual(entity.prop2, "value2")
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_accept_a_valid_uuid(self):
        expected_uuid = UniqueEntityId('cf28b7b2-a8af-4bd1-9d5b-b4c9917d340c')
        entity = StubEntity(unique_entity_id=expected_uuid, prop1='value1', prop2='value2')
        self.assertEqual(entity.unique_entity_id.id, expected_uuid.id)

    def test_to_dict_method(self):
        expected_dict = {
            "prop1": "value1",
            "prop2": "value2"
        }
        entity = StubEntity(**expected_dict)
        expected_dict = {"id": entity.id, **expected_dict}
        self.assertDictEqual(entity.to_dict(), expected_dict)
