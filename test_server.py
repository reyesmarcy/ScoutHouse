"""Test suite for testing Flask."""

import server
import unittest


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    def setUp(self):
        """Code to run before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"View Homes", result.data)

    def test_userinfo(self):
        """Does the correct form show up on the enter userinfo page?"""

        result = self.client.get("/userinfo")
        self.assertIn(b"Enter Some Basic Info", result.data)

    # def test_show_userinfo_exists(self):
    #     """When signing up, does it say a user already exists?"""

    #     user_info = {'email': 'cat@dog.com',
    #                 'password': 'catdog',
    #                 'salary': 200000,
    #                 'downpayment': 200000,
    #                 'debts': 500}

    #     result = self.client.post("/userinfo", data=user_info,
    #                               follow_redirects=True)

    #     self.assertIn(b"This user already exists", result.data)

    # def test_show_userinfo_new(self):
    #     """When signing up, does it redirect correctly for new users?"""

    #     user_info = {'email': 'zebra@zebra.com',
    #                 'password': 'zebra',
    #                 'salary': 200000,
    #                 'downpayment': 200000,
    #                 'debts': 500}
        
    #     result = self.client.post("/userinfo", data=user_info,
    #                               follow_redirects=True)

    #     self.assertIn(b"View Homes", result.data)

    # def test_login(self):
    #     """Does login page render correctly?"""

    #     result = self.client.get("/login")

if __name__ == "__main__":
    unittest.main()