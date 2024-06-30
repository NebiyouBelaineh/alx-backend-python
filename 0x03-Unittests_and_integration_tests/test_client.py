#!/usr/bin/env python3
"""Module to test client.GithubOrgClient class"""
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized, parameterized_class
import client
import fixtures
import requests
from fixtures import TEST_PAYLOAD


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


@parameterized_class(('org_payload',
                      'repos_payload',
                      'expected_repos',
                      'apache2_repos'),
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient"""
    @classmethod
    def setUpClass(cls):
        """Set up class method to start patching."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == 'https://api.github.com/orgs/google':
                response = Mock()
                response.json.return_value = cls.org_payload
                return response
            elif url == 'https://api.github.com/orgs/google/repos':
                response = Mock()
                response.json.return_value = cls.repos_payload
                return response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop patching."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method."""
        cli = client.GithubOrgClient('google')
        self.assertEqual(cli.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter."""
        cli = client.GithubOrgClient('google')
        self.assertEqual(cli.public_repos('apache-2.0'), self.apache2_repos)
