#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name))

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns expected URL."""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            client = GithubOrgClient("google")
            result = client._public_repos_url
            expected = "https://api.github.com/orgs/google/repos"
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
