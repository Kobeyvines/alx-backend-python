#!/usr/bin/env python3
"""Unit tests for GithubOrgClient behavior."""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org property fetches correct data."""
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"login": org_name})
        mock_get_json.assert_called_once_with(url)

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected URL."""
        with patch.object(
            GithubOrgClient, "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "some_url"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "some_url")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns repo names."""
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        with patch.object(
            GithubOrgClient, "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "url"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("url")
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": org,
        "repos_payload": repos,
        "expected_repos": expected,
        "apache2_repos": apache,
    }
    for org, repos, expected, apache in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide patcher for requests.get."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            MagicMock(json=lambda: cls.org_payload),
            MagicMock(json=lambda: cls.repos_payload),
            MagicMock(json=lambda: cls.org_payload),
            MagicMock(json=lambda: cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos integration."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
