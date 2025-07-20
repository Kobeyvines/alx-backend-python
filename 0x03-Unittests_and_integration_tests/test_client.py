#!/usr/bin/env python3
"""Unit tests validating GithubOrgClient implementation."""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class GithubOrgClientUnitTests(unittest.TestCase):
    """Unit test suite for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_fetch_org(self, org_name: str, mock_get_json) -> None:
        """Check whether GithubOrgClient.org returns correct data."""
        api_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"login": org_name}

        org_client = GithubOrgClient(org_name)
        org_details = org_client.org

        mock_get_json.assert_called_once_with(api_url)
        self.assertEqual(org_details, {"login": org_name})

    def test_repos_api_url(self) -> None:
        """Ensure _public_repos_url returns the proper repos API endpoint."""
        expected_url = "https://api.github.com/orgs/sample/repos"
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            client = GithubOrgClient("sample")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_retrieve_public_repos(self, mock_get_json):
        """Test retrieval of repository names from API payload."""
        mock_get_json.return_value = [
            {"name": "alpha", "license": {"key": "mit"}},
            {"name": "beta", "license": {"key": "apache-2.0"}},
            {"name": "gamma", "license": {"key": "mit"}},
        ]

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/sample/repos"
            client = GithubOrgClient("sample")
            repos = client.public_repos()

            expected_names = ["alpha", "beta", "gamma"]
            self.assertEqual(repos, expected_names)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url.return_value)

    @parameterized.expand([
        ({"license": {"key": "desired_license"}}, "desired_license", True),
        ({"license": {"key": "other_license"}}, "desired_license", False),
    ])
    def test_license_check(self, repo_data, target_license, outcome):
        """Test has_license static method for correct boolean output."""
        result = GithubOrgClient.has_license(repo_data, target_license)
        self.assertEqual(result, outcome)


@parameterized_class([
    {
        "org_payload": org,
        "repos_payload": repos,
        "expected_repos": expected,
        "apache2_repos": apache,
    }
    for org, repos, expected, apache in TEST_PAYLOAD
])
class GithubOrgClientIntegrationTests(unittest.TestCase):
    """Integration testing class for GithubOrgClient methods."""

    @classmethod
    def setUpClass(cls):
        """Setup mocks for integration tests."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = [
            MagicMock(json=lambda: cls.org_payload),
            MagicMock(json=lambda: cls.repos_payload),
            MagicMock(json=lambda: cls.org_payload),
            MagicMock(json=lambda: cls.repos_payload),
        ]

@classmethod
def tearDownClass(cls):
    """Stop all mocks after tests complete."""
    cls.get_patcher.stop()

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get mock."""
        cls.get_patcher.stop()

    @classmethod
    def _start_mocked_requests(cls):
        cls.get_patcher = patch("requests.get")
        mock_request = cls.get_patcher.start()
        mock_request.side_effect = cls._generate_mock_responses()

    @classmethod
    def _generate_mock_responses(cls):
        return [
            MagicMock(json=lambda: cls.org_payload),
            MagicMock(json=lambda: cls.repos_payload),
            MagicMock(json=lambda: cls.org_payload),
            MagicMock(json=lambda: cls.repos_payload),
        ]

    def test_fetching_all_repos(self):
        """Test public_repos returns expected repo list."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_repos_with_license_filter(self):
        """Test filtering repos by apache-2.0 license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
