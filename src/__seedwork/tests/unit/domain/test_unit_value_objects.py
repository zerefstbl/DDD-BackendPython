import unittest
from unittest.mock import patch

import json

import uuid

from dataclasses import dataclass, is_dataclass, FrozenInstanceError

from __seedwork.domain.value_objects import ValueObject, UniqueEntityId

from __seedwork.domain.exceptions import InvalidUuidException

from abc import ABC


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str


@dataclass(frozen=True)
class StubTwoProps(ValueObject):
    prop1: str
    prop2: str


class TestValueObject(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    def test_if_is_abc_class(self):
        self.assertTrue(isinstance(ValueObject(), ABC))

    def test_return_string_if_has_one_prop(self):
        prop = "Prop"
        value_object = StubOneProp(prop=prop)
        self.assertEqual(str(value_object), prop)

    def test_return_dict_if_has_more_one_prop(self):
        props = json.dumps({
            "prop1": "prop1",
            "prop2": "prop2",
        })
        value_object = StubTwoProps(**json.loads(props))
        self.assertEqual(props, str(value_object))

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = StubOneProp(prop="prop")
            value_object.prop = "New Value"


class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throws_except_when_uuid_is_invalid(self):
        with patch.object(UniqueEntityId, '_UniqueEntityId__validate', autospec=True, side_effect=UniqueEntityId._UniqueEntityId__validate) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId('fake id')
            mock_validate.assert_called_once()
            self.assertEqual(
                assert_error.exception.args[0], 'ID must be a valid UUID')

    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(UniqueEntityId, '_UniqueEntityId__validate', autospec=True, side_effect=UniqueEntityId._UniqueEntityId__validate) as mock_validate:
            expected_uuid = '3aefc22e-8006-4024-a239-a27084c5133e'

            value_object = UniqueEntityId(expected_uuid)

            mock_validate.assert_called_once()

            self.assertEqual(value_object.id, expected_uuid)

        uuid_value = uuid.uuid4()

        new_value_object = UniqueEntityId(uuid_value)

        self.assertTrue(isinstance(new_value_object.id, str))

    def test_generate_id_when_no_passed_id_in_constructor(self):
        with patch.object(UniqueEntityId, '_UniqueEntityId__validate', autospec=True, side_effect=UniqueEntityId._UniqueEntityId__validate) as mock_validate:
            value_object = UniqueEntityId()
            self.assertTrue(uuid.UUID(value_object.id))
            mock_validate.assert_called_once()

    def test_is_imutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = 'TESTE'

    def test_if_return_string(self):
        value_object = UniqueEntityId()
        self.assertEqual(str(value_object), value_object.id)
