import unittest
from pathlib import Path

from PIL import Image

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
        self.assertIn(b"$1,120", response.data)
        self.assertNotIn(b"$0.01", response.data)
        self.assertNotIn(b"Ll\xc3\xa9vate Original", response.data)
        self.assertNotIn(b"Solo Original", response.data)
        self.assertNotIn(b"Lo que define", response.data)
        self.assertNotIn(b"Una bolsa", response.data)
        self.assertNotIn(b"Toda su ficha", response.data)
        self.assertNotIn(b"Referencia visual", response.data)
        self.assertNotIn(b"Referencia ", response.data)
        self.assertIn(b'data-language', response.data)
        self.assertIn(b'css/style.css?v=28', response.data)
        self.assertIn(b'js/i18n.js?v=14', response.data)
        self.assertIn(b'js/app.js?v=30', response.data)
        self.assertIn(b'data-catalog-name="811140"', response.data)
        self.assertIn(b'data-catalog-image="811920"', response.data)
        self.assertIn(b'data-catalog-name="634210"', response.data)
        self.assertIn(b'data-catalog-name="802150"', response.data)
        self.assertNotIn(b'id="brands"', response.data)
        self.assertNotIn(b'href="#brands"', response.data)
        self.assertIn(b'data-department-filter="noodles"', response.data)
        self.assertIn(b'data-department-filter="snacks"', response.data)
        self.assertEqual(response.data.count(b'data-catalog-detail="'), 83)
        self.assertEqual(response.data.count(b'data-catalog-quantity="'), 83)
        self.assertEqual(response.data.count(b'data-catalog-heat="'), 83)
        self.assertEqual(response.data.count(b'data-card="'), 83)
        self.assertEqual(response.data.count(b'data-select="'), 83)
        self.assertEqual(response.data.count(b'data-card-product="'), 83)
        self.assertEqual(response.data.count(b'data-select-product="'), 83)
        self.assertEqual(response.data.count(b'data-search-product="'), 83)
        self.assertEqual(response.data.count(b'data-catalog-spice="'), 37)
        self.assertIn(b'data-catalog-spice="811130"', response.data)
        self.assertIn(b'data-catalog-spice="634280"', response.data)
        self.assertEqual(response.data.count(b'/assets/refrescos/cutouts/'), 71)
        self.assertLess(response.data.index(b'data-card-product="811120"'), response.data.index(b'data-card-product="811140"'))
        self.assertLess(response.data.index(b'data-card-product="811140"'), response.data.index(b'data-card-product="811150"'))
        self.assertLess(response.data.index(b'data-card-product="811650"'), response.data.index(b'data-card-product="811910"'))
        self.assertIn(b'data-clear-cart', response.data)
        self.assertIn(b'data-whatsapp-quote', response.data)
        self.assertIn(b'Cotizar por WhatsApp', response.data)
        self.assertIn(b'data-story-section', response.data)
        self.assertIn(b'Tu carrito', response.data)
        self.assertIn(b"T\xc3\xa9rminos y condiciones", response.data)
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

    def test_whatsapp_quote_targets_requested_number(self):
        response = self.client.get("/js/app.js")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'const WHATSAPP_NUMBER = "5229723373"', response.data)
        self.assertIn(b"https://wa.me/${WHATSAPP_NUMBER}", response.data)
        self.assertIn(b"buildWhatsAppMessage", response.data)

    def test_products_have_complete_selected_flavor_content(self):
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        for product in response.get_json()["products"]:
            self.assertEqual(len(product["directions"]), 4)
            self.assertEqual(len(product["recommendations"]), 3)
            self.assertTrue(product["prepared_image"].startswith("/assets/prepared-"))
            self.assertGreater(product["price"], 1)
            self.assertTrue(product["price_label"].startswith("$"))

    def test_catalog_has_all_references_and_images(self):
        response = self.client.get("/api/catalog")
        self.assertEqual(response.status_code, 200)
        catalog = response.get_json()["products"]
        self.assertEqual(len(catalog), 83)
        self.assertEqual({item["sku"] for item in catalog}.__len__(), 83)
        self.assertIn("Agotado", next(item["status"] for item in catalog if item["sku"] == "811720"))
        self.assertEqual(next(item["brand"] for item in catalog if item["sku"] == "634210"), "Master Kong")
        self.assertEqual(next(item["category"] for item in catalog if item["sku"] == "802150"), "chips")
        self.assertEqual(next(item["category"] for item in catalog if item["sku"] == "807331"), "cookies")
        self.assertEqual(next(item["category"] for item in catalog if item["sku"] == "851120"), "candy")
        self.assertEqual(next(item["category"] for item in catalog if item["sku"] == "061010"), "bakery")
        for item in catalog:
            self.assertGreater(item["price"], 1, item["sku"])
            self.assertTrue(item["price_label"].startswith("$"), item["sku"])
            self.assertGreaterEqual(item["units_per_case"], 1, item["sku"])
            self.assertIn(" de ", item["pack_label"], item["sku"])
            self.assertTrue(item["image"].startswith("/assets/"), item["sku"])
            self.assertTrue(item["source_url"].startswith("https://"), item["sku"])
            self.assertNotIn("google.com/search", item["source_url"], item["sku"])
            self.assertTrue(item["description_verified"], item["sku"])
            self.assertIn(item["heat_level"], range(6), item["sku"])
            self.assertEqual(item["heat"], item["heat_level"] * 20, item["sku"])
            self.assertTrue(item["heat_label_es"].endswith("/5"), item["sku"])
            self.assertTrue(item["heat_label_en"].endswith("/5"), item["sku"])
            self.assertTrue(item["heat_label_zh"].endswith("/5"), item["sku"])
            self.assertTrue(item["name_es"], item["sku"])
            self.assertTrue(item["name_en"], item["sku"])
            self.assertTrue(item["name_zh"], item["sku"])
            self.assertTrue(item["description_es"], item["sku"])
            self.assertTrue(item["description_en"], item["sku"])
            self.assertTrue(item["description_zh"], item["sku"])
            image_response = self.client.get(item["image"].split("?")[0])
            try:
                self.assertEqual(image_response.status_code, 200, item["sku"])
                self.assertGreater(len(image_response.get_data()), 1000, item["sku"])
            finally:
                image_response.close()

        spicy_items = [
            item for item in catalog
            if item["category"] in {"soups", "bowls", "tteokbokki"}
        ]
        self.assertEqual(len(spicy_items), 37)
        for item in spicy_items:
            self.assertIn(item["spice_level"], range(1, 6), item["sku"])

    def test_checkout_accepts_catalog_products_at_case_price(self):
        invalid = self.client.post("/api/checkout", json={"cart": []})
        self.assertEqual(invalid.status_code, 400)

        valid = self.client.post(
            "/api/checkout",
            json={
                "customer": {"name": "Test Customer", "email": "test@example.com"},
                "cart": [
                    {"id": "811140", "quantity": 2},
                    {"id": "811120", "quantity": 3},
                ],
            },
        )
        payload = valid.get_json()
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(len(payload["items"]), 2)
        # 811140 and 811120 are both $1,120 per case: 2 + 3 cases = $5,600.
        self.assertEqual(payload["subtotal"], "5600.00")
        self.assertEqual(payload["shipping"], "0.00")
        self.assertEqual(payload["total"], "5600.00")

    def test_checkout_accepts_new_noodle_and_chip_products(self):
        response = self.client.post(
            "/api/checkout",
            json={
                "customer": {"name": "Test Customer", "email": "test@example.com"},
                "cart": [
                    {"id": "634210", "quantity": 1},
                    {"id": "802150", "quantity": 2},
                ],
            },
        )
        payload = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(payload["items"]), 2)
        self.assertEqual(payload["subtotal"], "2331.00")
        self.assertEqual(payload["total"], "2331.00")

    def test_refrescos_catalog_is_wholesale_with_real_photos(self):
        response = self.client.get("/api/refrescos")
        self.assertEqual(response.status_code, 200)
        drinks = response.get_json()["products"]
        self.assertEqual(len(drinks), 71)
        self.assertEqual(len({item["sku"] for item in drinks}), 71)
        self.assertEqual(next(item["name_zh"] for item in drinks if item["sku"] == "832120"), "康师傅冰红茶")
        self.assertEqual(next(item["brand"] for item in drinks if item["sku"] == "837110"), "Red Bull")
        for item in drinks:
            self.assertTrue(item["image"].startswith("/assets/refrescos/"), item["sku"])
            self.assertIn(item["sku"], item["image"])
            self.assertGreater(item["price"], 1, item["sku"])
            self.assertGreaterEqual(item["units_per_case"], 8, item["sku"])
            self.assertIn(" de ", item["pack_label"], item["sku"])
            self.assertTrue(item["name_es"], item["sku"])
            self.assertTrue(item["name_en"], item["sku"])
            self.assertTrue(item["name_zh"], item["sku"])
            self.assertTrue(item["description_es"], item["sku"])
            self.assertTrue(item["description_en"], item["sku"])
            self.assertTrue(item["description_zh"], item["sku"])
            image_response = self.client.get(item["image"].split("?")[0])
            try:
                self.assertEqual(image_response.status_code, 200, item["sku"])
                self.assertGreater(len(image_response.get_data()), 4000, item["sku"])
            finally:
                image_response.close()
            cutout_path = item["image"].split("?")[0].replace("/refrescos/", "/refrescos/cutouts/")
            cutout_response = self.client.get(cutout_path)
            try:
                self.assertEqual(cutout_response.status_code, 200, item["sku"])
                self.assertGreater(len(cutout_response.get_data()), 4000, item["sku"])
            finally:
                cutout_response.close()

    def test_all_refresco_assets_are_hd_and_cutouts_are_transparent(self):
        asset_root = Path(__file__).resolve().parents[1] / "frontend" / "assets" / "refrescos"
        originals = sorted(asset_root.glob("*.webp"))
        cutouts = sorted((asset_root / "cutouts").glob("*.webp"))
        self.assertEqual(len(originals), 71)
        self.assertEqual({path.name for path in originals}, {path.name for path in cutouts})

        for original_path in originals:
            with Image.open(original_path) as original:
                original.verify()
            with Image.open(original_path) as original:
                self.assertEqual(original.size, (1600, 1600), original_path.name)

            with Image.open(asset_root / "cutouts" / original_path.name) as cutout:
                cutout.verify()
            with Image.open(asset_root / "cutouts" / original_path.name) as cutout:
                self.assertIn("A", cutout.getbands(), original_path.name)
                self.assertGreaterEqual(max(cutout.size), 1000, original_path.name)

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
