#!/usr/bin/env python3
"""Test module for utils.access_nested_map() method"""
from unittest import TestCase
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(TestCase):
    """TestAccessNestedMap class to test utils.access_nested_map()"""

    @parameterized.expand([
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test method"""
        self.assertEqual(access_nested_map(nested_map, path), expected)
