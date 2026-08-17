import unittest

from app import app


class ShowroomTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pick your burn", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_checkout_validates_and_confirms(self):
        invalid = self.client.post("/api/checkout", json={"cart": []})
        self.assertEqual(invalid.status_code, 400)

        valid = self.client.post(
            "/api/checkout",
            json={
                "customer": {"name": "Test Customer", "email": "test@example.com"},
                "cart": [{"id": "carbonara", "quantity": 2}],
            },
        )
        payload = valid.get_json()
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(payload["status"], "confirmed")
        self.assertEqual(payload["subtotal"], "4.98")


if __name__ == "__main__":
    unittest.main()
