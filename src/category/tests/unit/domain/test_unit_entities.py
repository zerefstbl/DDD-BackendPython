from dataclasses import is_dataclass

import unittest

from category.domain.entities import Category

from datetime import datetime



class TestCategory(unittest.TestCase):


    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))
    
    
    def test_constructor(self):
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
        category1 = Category(name='Movie')
        category2 = Category(name='Movie2')
        
        self.assertNotEqual(
            category1.created_at.timestamp(),
            category2.created_at.timestamp()
        )
    
    