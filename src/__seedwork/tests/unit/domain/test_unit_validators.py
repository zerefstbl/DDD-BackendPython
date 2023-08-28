import unittest

from __seedwork.domain.validators import ValidatorRules, ValidatorFieldsInterface
from __seedwork.domain.exceptions import ValidationException

from dataclasses import fields


class TestValidatorRules(unittest.TestCase):
    def test_values_method(self):
        expected_value = "Some value"
        expected_prop = 'prop'
        validator = ValidatorRules.values(expected_value, expected_prop)
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, expected_value)

    def test_required_rules(self):
        self.assertIsInstance(
            ValidatorRules.values('Some Value', 'prop').required(),
            ValidatorRules
        )

    def test_required_rule_with_none_values(self):
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(None, 'prop').required()
        self.assertEqual(
            assert_error.exception.args[0], 'The prop is required')

    def test_required_rule_with_empty_value(self):
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values('', 'prop').required()
        self.assertEqual(
            assert_error.exception.args[0], 'The prop is required')

    def test_string_rule(self):
        invalid_data = [
            {"value": 5, "prop": "prop"},
            {"value": True, "prop": "prop"},
            {"value": {}, "prop": "prop"},
        ]

        for data in invalid_data:
            with self.assertRaises(ValidationException, msg=f"{data}") as assert_error:
                validator = ValidatorRules.values(data['value'], data['prop'])
                validator.string()
            self.assertEqual(
                assert_error.exception.args[0], f'The {data["prop"]} must be a string', f"{data}")

        valid_data = [
            {"value": "String", "prop": "prop"},
            {"value": "", "prop": "prop"},
            {"value": None, "prop": "prop"},
        ]

        for data in valid_data:
            validator = ValidatorRules.values(
                data['value'], data['prop']).string()

            self.assertEqual(data['value'], validator.value)
            self.assertIsInstance(
                validator,
                ValidatorRules
            )

    def test_max_length_rule(self):
        invalid_value = 't' * 5
        prop = 'prop'
        max_length = 4

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(invalid_value, prop).max_length(max_length)

        self.assertEqual(
            assert_error.exception.args[0], f'The {prop} must be less than {max_length}')

        valid_value = 't' * 4
        self.assertIsInstance(
            ValidatorRules.values(valid_value, prop).max_length(max_length),
            ValidatorRules
        )

    def test_boolean_rule(self):
        invalid_data = [
            {"value": 5, "prop": "prop"},
            {"value": 'True', "prop": "prop"},
            {"value": '', "prop": "prop"},
            {"value": {}, "prop": "prop"},
        ]

        for data in invalid_data:
            with self.assertRaises(ValidationException, msg=f"{data}") as assert_error:
                validator = ValidatorRules.values(data['value'], data['prop'])
                validator.boolean()
            self.assertEqual(
                assert_error.exception.args[0], f'The {data["prop"]} must be a boolean', f"{data}")

        valid_data = [
            {"value": True, "prop": "prop"},
            {"value": False, "prop": "prop"},
            {"value": None, "prop": "prop"},
        ]

        for data in valid_data:
            validator = ValidatorRules.values(
                data['value'], data['prop']).boolean()

            self.assertEqual(data['value'], validator.value)
            self.assertIsInstance(
                validator,
                ValidatorRules
            )

    def test_throw_a_validation_exception_when_combine_two_or_more_rules(self):
        with self.assertRaises(ValidationException) as assert_error:
            validator = ValidatorRules.values(None, 'prop1')
            validator = validator.required().string().max_length(max_length=1)

        self.assertEqual(
            assert_error.exception.args[0], "The prop1 is required")

        with self.assertRaises(ValidationException) as assert_error:
            validator = ValidatorRules.values(True, 'prop1')
            validator.required().string().max_length(max_length=1)
        self.assertEqual(
            assert_error.exception.args[0], 'The prop1 must be a string')

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values('Values', 'prop1').required(
            ).string().max_length(max_length=2)

        self.assertEqual(
            assert_error.exception.args[0], 'The prop1 must be less than 2')

    def test_valid_cases_with_combination_rules(self):
        ValidatorRules.values('value', 'prop').required().string()
        ValidatorRules.values(
            'value', 'prop').required().string().max_length(5)
        ValidatorRules.values(True, 'prop').required().boolean()
        ValidatorRules.values(False, 'prop').required().boolean()
        self.assertTrue(True)  # pylint: disable=redundant-unittest-assert


class TestValidatorFieldsInterface(unittest.TestCase):

    def test_throw_error_when_validate_method_is_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            # pylint: disable=no-value-for-parameter
            ValidatorFieldsInterface()
        self.assertEqual(
            assert_error.exception.args[0], "Can't instantiate abstract class ValidatorFieldsInterface with abstract method validate")

    def test_init_none(self):  # sourcery skip: extract-duplicate-method
        fields_class = fields(ValidatorFieldsInterface)
        errors_field = fields_class[0]
        self.assertEqual(errors_field.name, 'errors')
        self.assertIsNone(errors_field.default)

        validated_data_field = fields_class[1]
        self.assertEqual(validated_data_field.name, 'validated_data')
        self.assertIsNone(validated_data_field.default)
