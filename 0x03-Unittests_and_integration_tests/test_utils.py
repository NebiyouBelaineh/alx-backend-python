#!/usr/bin/env python3
"""Test module for utils.access_nested_map() method"""
from unittest import TestCase
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(TestCase):
    """TestAccessNestedMap class to test utils.access_nested_map()"""

    @parameterized.expand([
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test method for expected output"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError('a')),
        ({"a": 1}, ("a", "b"), KeyError('b')),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """Test method for raising exception"""
        self.assertRaises(KeyError)


class TestGetJson(TestCase):
    """class to test utils.get_json()"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Tests get_json()"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(TestCase):
    """Test class for memoize decorator"""
    def test_memoize(self):
        """Test memoize"""
        class TestClass:
            """Test class"""
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass,
                          'a_method',
                          return_value=42) as mock_a_method:
            my_test = TestClass()

            # a_property called with no parenthesis because
            # memoize makes it a property
            res_1 = my_test.a_property
            res_2 = my_test.a_property

            self.assertEqual(res_1, 42)
            self.assertEqual(res_2, 42)

            mock_a_method.assert_called_once()
