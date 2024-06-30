#!/usr/bin/env python3
"""Module to test client.GithubOrgClient class"""
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
import client


class TestGithubOrgClient(unittest.TestCase):
    """Test cass for client.GithubOrgClient class"""
    @parameterized.expand([
        ('google'),
        ('abc'),
    ])
    @patch('client.get_json')
    def test_org(self, org, mock_org):
        """Test org methood"""
        instance = client.GithubOrgClient(org_name=org)

        instance.org
        # self.assertEqual(result, response)
        org_url = f"https://api.github.com/orgs/{org}"
        mock_org.assert_called_once_with(org_url)

    def test_public_repos_url(self):
        """Tests _public_repos_url method"""
        with patch.object(client.GithubOrgClient,
                          '_public_repos_url',
                          new_callable=unittest.mock.PropertyMock
                          ) as mock_a_property:
            mocked_url = "https://api.github.com/mocked_url"
            mock_a_property.return_value = mocked_url
            instance = client.GithubOrgClient(org_name='google')
            self.assertEqual(instance._public_repos_url, mocked_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method from client.GithubOrgClient"""
        with patch.object(client.GithubOrgClient,
                          '_public_repos_url',
                          new_callable=unittest.mock.PropertyMock
                          ) as mock_a_property:
            mocked_url = "https://api.github.com/mocked_url"
            mock_a_property.return_value = mocked_url

            mock_get_json.return_value = [
                {'name': 'google', 'license': {'key': 'license1'}},
                {'name': 'apple', 'license': {'key': 'license2'}},
                {'name': 'microsoft', 'license': {'key': 'license1'}},
            ]

            instance = client.GithubOrgClient(org_name='google')

            result = instance.public_repos()
            expected_res = ['google', 'apple', 'microsoft']
            self.assertEqual(result, expected_res)

            mock_get_json.assert_called_once()
            mock_a_property.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test static method has_license"""
        result = client.GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
