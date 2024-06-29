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
