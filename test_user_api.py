
import os
import unittest
import requests

class TestUserAPI(unittest.TestCase):
    """Unit tests for User API endpoints."""

    def setUp(self):
        # Base configuration
        self.base_url = os.getenv("USER_API_BASE_URL", "https://api.example.com/users")
        # Optional auth header using a token, if provided as env var
        token = os.getenv("API_TOKEN")
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    def tearDown(self):
        # Cleanup hooks if needed
        pass

    def test_get_user_success(self):
        """GET /users/{id} returns 200 and correct payload."""
        user_id = 1
        url = f"{self.base_url}/{user_id}"
        response = requests.get(url, headers=self.headers, timeout=10)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["id"], user_id)
        # Optional header checks
        self.assertIn("Content-Type", response.headers)
        self.assertTrue(response.headers["Content-Type"].startswith("application/json"))

    def test_get_user_not_found(self):
        """GET /users/{id} returns 404 for unknown user."""
        user_id = 999999
        url = f"{self.base_url}/{user_id}"
        response = requests.get(url, headers=self.headers, timeout=10)

        self.assertEqual(response.status_code, 404)
        body = response.json()
        # Expect a standardized error envelope
        self.assertIn("error", body)
        self.assertIn("message", body)

    def test_create_user_validation_error(self):
        """POST /users returns 400 when required fields are missing."""
        url = f"{self.base_url}"
        payload = {
            # Missing required fields like 'email' or 'password'
            "name": "Deepthi"
        }
        response = requests.post(url, json=payload, headers=self.headers, timeout=10)

        self.assertEqual(response.status_code, 400)
        errors = response.json()
        self.assertIn("errors", errors)
        self.assertIn("email", errors["errors"])  # example field error

if __name__ == "__main__":
    unittest.main()
