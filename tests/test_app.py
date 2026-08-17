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
        self.assertIn(b"811920", response.data)
        self.assertIn(b"Todos los productos", response.data)
        self.assertIn(b"$0.01", response.data)
        self.assertNotIn(b"Ll\xc3\xa9vate Original", response.data)
        self.assertNotIn(b"Solo Original", response.data)
        self.assertNotIn(b"Lo que define", response.data)
        self.assertIn(b"prepared-carbonara.jpg?v=3", response.data)
        favicon = self.client.get("/assets/favicon.svg")
        try:
            self.assertEqual(favicon.status_code, 200)
        finally:
            favicon.close()

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
            self.assertEqual(product["price"], 0.01)
            self.assertEqual(product["price_label"], "$0.01")

    def test_catalog_has_all_references_and_images(self):
        response = self.client.get("/api/catalog")
        self.assertEqual(response.status_code, 200)
        catalog = response.get_json()["products"]
        self.assertEqual(len(catalog), 22)
        self.assertEqual({item["sku"] for item in catalog}.__len__(), 22)
        self.assertIn("Agotado", next(item["status"] for item in catalog if item["sku"] == "811720"))
        for item in catalog:
            self.assertEqual(item["price"], 0.01)
            self.assertEqual(item["price_label"], "$0.01")
            self.assertTrue(item["image"].endswith("?v=3"), item["sku"])
            self.assertTrue(item["source_url"].startswith("https://buldak.com/"), item["sku"])
            image_response = self.client.get(item["image"].split("?")[0])
            try:
                self.assertEqual(image_response.status_code, 200, item["sku"])
                self.assertGreater(len(image_response.get_data()), 1000, item["sku"])
            finally:
                image_response.close()

    def test_checkout_accepts_catalog_products_at_provisional_price(self):
        invalid = self.client.post("/api/checkout", json={"cart": []})
        self.assertEqual(invalid.status_code, 400)

        valid = self.client.post(
            "/api/checkout",
            json={
                "customer": {"name": "Test Customer", "email": "test@example.com"},
                "cart": [{"id": "811140", "quantity": 2}],
            },
        )
        payload = valid.get_json()
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(payload["subtotal"], "0.02")
        self.assertEqual(payload["shipping"], "0.00")
        self.assertEqual(payload["total"], "0.02")

    def test_checkout_rejects_sold_out_product(self):
        response = self.client.post(
            "/api/checkout",
            json={
                "customer": {"name": "Test Customer", "email": "test@example.com"},
                "cart": [{"id": "811720", "quantity": 1}],
            },
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
