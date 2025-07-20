#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map."""

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test access_nested_map raises KeyError with expected message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")

if __name__ == "__main__":
    unittest.main()
