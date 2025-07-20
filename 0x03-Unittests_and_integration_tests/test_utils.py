#!/usr/bin/env python3
"""Unit tests for utils.memoize
"""
import unittest
from unittest.mock import patch
from utils import memoize

class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result and calls the method only once."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()

if __name__ == "__main__":
    unittest.main()
