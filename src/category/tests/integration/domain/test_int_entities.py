import unittest

from __seedwork.domain.exceptions import ValidationException

from category.domain.entities import Category


class TestCategoryIntegrations(unittest.TestCase):

    valid_name = "Valid Name"
    valid_description = "Valid Name"

    def test_create_with_invalid_cases_for_name_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name=None)
        self.assertEqual(
            assert_error.exception.args[0], 'The name is required')

        with self.assertRaises(ValidationException) as assert_error:
            Category(name='')
        self.assertEqual(
            assert_error.exception.args[0], 'The name is required')

        with self.assertRaises(ValidationException) as assert_error:
            Category(name=True)
        self.assertEqual(
            assert_error.exception.args[0], 'The name must be a string'
        )

        with self.assertRaises(ValidationException) as assert_error:
            Category(name='t' * 256)
        self.assertEqual(
            assert_error.exception.args[0],
            'The name must be less than 255'
        )

    def test_create_with_invalid_case_for_description_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name="Valid name", description=False)
        self.assertEqual(
            assert_error.exception.args[0], 'The description must be a string')

    def test_create_with_invalid_case_for_is_active_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name='Valid Name', description='Valid Description',
                     is_active='Invalid IsActive')
        self.assertEqual(
            assert_error.exception.args[0],
            'The is_active must be a boolean'
        )

    def test_create_with_valid_cases(self):
        try:
            Category(name=self.valid_name)
            Category(name=self.valid_name, description=None)
            Category(name=self.valid_name, description='')
            Category(name=self.valid_name, is_active=True)
            Category(name=self.valid_name, is_active=False)
            Category(name=self.valid_name,
                     description='Some description', is_active=False)

        except ValidationException as exception:
            self.fail(f'Some prop is not valid. Error: {exception.args[0]}')

    def test_update_with_invalid_cases_for_name_prop(self):
        category = Category(name=self.valid_name)
        with self.assertRaises(ValidationException) as assert_error:
            category.update(name=None, description="")
        self.assertEqual(
            assert_error.exception.args[0], 'The name is required')

        with self.assertRaises(ValidationException) as assert_error:
            category.update(name='', description="")
        self.assertEqual(
            assert_error.exception.args[0], 'The name is required')

        with self.assertRaises(ValidationException) as assert_error:
            category.update(name=True, description="")
        self.assertEqual(
            assert_error.exception.args[0], 'The name must be a string'
        )

        with self.assertRaises(ValidationException) as assert_error:
            category.update(
                name='t' * 256, description='')
        self.assertEqual(
            assert_error.exception.args[0],
            'The name must be less than 255'
        )

    def test_update_with_invalid_case_for_description_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name="Valid name").update(
                name=self.valid_name, description=False)
        self.assertEqual(
            assert_error.exception.args[0], 'The description must be a string')

    def test_update_with_valid_cases(self):
        category = Category(name=self.valid_name, description=None)
        try:
            category.update(
                name=self.valid_name, description=None)
            category.update(
                name=self.valid_name, description='')

        except ValidationException as exception:
            self.fail(f'Some prop is not valid. Error: {exception.args[0]}')
