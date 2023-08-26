from dataclasses import is_dataclass, FrozenInstanceError

import unittest
from unittest.mock import patch

from category.domain.entities import Category

from datetime import datetime


class TestCategory(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        with patch.object(Category, 'validate') as mock_validate:
            category = Category(
                name='Movie',
                description='Some Description',
                is_active=False,
                created_at=datetime.now()
            )

            self.assertEqual(category.name, 'Movie')
            self.assertEqual(category.description, 'Some Description')
            self.assertEqual(category.is_active, False)
            self.assertIsInstance(category.created_at, datetime)

    def test_if_created_at_is_generated_in_constructor(self):
        with patch.object(Category, 'validate') as mock_validate:
            category1 = Category(name='Movie')
            category2 = Category(name='Movie2')

            self.assertNotEqual(
                category1.created_at.timestamp(),
                category2.created_at.timestamp()
            )

    def test_is_imutable(self):
        with patch.object(Category, 'validate') as mock_validate:
            with self.assertRaises(FrozenInstanceError):
                category = Category(name="Nome da Categoria")
                category.name = "New Name"

    def test_update_category(self):
        with patch.object(Category, 'validate') as mock_validate:
            expected_name = 'Updated Name'
            expected_description = 'Updated Description'

            category = Category(name='Old Name')

            category.update(name=expected_name,
                            description=expected_description)

            self.assertEqual(expected_name, category.name)
            self.assertEqual(expected_description, category.description)

    def test_raise_exception_if_has_update_without_name_and_description(self):
        with patch.object(Category, 'validate') as mock_validate:
            category = Category(name='Name')
            with self.assertRaises(TypeError):
                # pylint: disable=no-value-for-parameter
                category.update()

    def test_inactive_category(self):
        with patch.object(Category, 'validate') as mock_validate:
            category = Category(name='Category')
            category.deactivate()

            self.assertFalse(category.is_active)

    def test_if_category_is_active(self):
        with patch.object(Category, 'validate') as mock_validate:
            category = Category(name="Category")
            self.assertTrue(category.is_active)
