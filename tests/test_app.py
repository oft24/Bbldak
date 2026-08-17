import unittest

from app import app


class ShowroomTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"BuldakShop", response.data)
        self.assertIn(b"811140", response.data)
        self.assertIn(b"prepared-carbonara.webp", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")
        self.assertEqual(response.get_json()["service"], "buldakshop")

    def test_products_have_complete_selected_flavor_content(self):
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        for product in response.get_json()["products"]:
            self.assertEqual(len(product["directions"]), 4)
            self.assertEqual(len(product["recommendations"]), 3)
            self.assertTrue(product["prepared_image"].startswith("/assets/prepared-"))

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
