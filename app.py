from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from secrets import token_hex

from flask import Flask, jsonify, render_template, request, send_from_directory


app = Flask(
    __name__,
    static_folder="public",
    static_url_path="",
    template_folder="templates",
)


PRODUCTS = [
    {
        "id": "carbonara",
        "number": "01",
        "name": "Carbonara",
        "tagline": "Creamy heat. Still dangerous.",
        "description": "Milk and cheese soften the burn without ever putting it out.",
        "price": 2.49,
        "weight": "130 g · single",
        "heat": 40,
        "heat_label": "Creamy heat",
        "shu": "1,200",
        "kcal": "530",
        "story_title": ["Creamy.", "Spicy.", "Dangerously easy."],
        "story": (
            "Four minutes in boiling water, drained, then folded through the sauce "
            "off the heat. The cream carries the capsaicin instead of cutting it, "
            "which is why the second bite is always hotter than the first."
        ),
        "ingredients": ["Cream", "Cheese", "Chili", "Noodles"],
        "image": "/assets/carbonara.png?v=1",
        "colors": {
            "bg_a": "#f5d9e1",
            "bg_b": "#fff8f4",
            "glow": "#ffc1d2",
            "ink": "#2b171e",
            "accent": "#b3123f",
        },
        "keywords": "carbonara carb creamy cream mild cheese pink",
    },
    {
        "id": "original",
        "number": "02",
        "name": "Original",
        "tagline": "The one that started the dare.",
        "description": "Clean, direct fire with nothing to hide behind.",
        "price": 2.29,
        "weight": "140 g · single",
        "heat": 82,
        "heat_label": "Hot",
        "shu": "4,404",
        "kcal": "540",
        "story_title": ["Direct.", "Dry.", "Unforgiving."],
        "story": (
            "No broth to dilute it and no dairy to soften it. The sauce goes on last "
            "and stays where it lands — the reason this one built the reputation."
        ),
        "ingredients": ["Chili", "Sesame", "Seaweed", "Noodles"],
        "image": "/assets/original.png?v=1",
        "colors": {
            "bg_a": "#120e0d",
            "bg_b": "#2a110b",
            "glow": "#ff642f",
            "ink": "#f8f2ef",
            "accent": "#ff5a20",
        },
        "keywords": "original hot extra spicy fire classic black ramen",
    },
    {
        "id": "quattro",
        "number": "03",
        "name": "Quattro Cheese",
        "tagline": "Four cheeses, late heat.",
        "description": "Rich and warm, with the heat arriving one beat late.",
        "price": 2.79,
        "weight": "145 g · single",
        "heat": 60,
        "heat_label": "Spicy",
        "shu": "2,600",
        "kcal": "560",
        "story_title": ["Rich.", "Warm.", "Slow to bite."],
        "story": (
            "Cheddar, gouda, mozzarella and parmesan melt into the sauce as it cools. "
            "The heat is still there — it just arrives behind the richness."
        ),
        "ingredients": ["Cheddar", "Gouda", "Cream", "Noodles"],
        "image": "/assets/quattro.png?v=1",
        "colors": {
            "bg_a": "#f3c45d",
            "bg_b": "#fff2d6",
            "glow": "#ffde8f",
            "ink": "#392608",
            "accent": "#b64b0c",
        },
        "keywords": "quattro cheese cheesy four rich orange swicy",
    },
]

PRODUCT_BY_ID = {product["id"]: product for product in PRODUCTS}
PRODUCT_ASSET_DIR = Path(__file__).resolve().parent / "assets"


@app.get("/")
def index():
    return render_template("index.html", products=PRODUCTS)


@app.get("/api/health")
def health():
    return jsonify(status="ok", service="buldak-showroom")


@app.get("/api/products")
def products():
    return jsonify(products=PRODUCTS)


@app.get("/assets/<path:filename>")
def product_asset(filename: str):
    """Serve product photography through Flask in every WSGI environment."""
    return send_from_directory(PRODUCT_ASSET_DIR, filename, max_age=31536000)


@app.post("/api/checkout")
def checkout():
    payload = request.get_json(silent=True) or {}
    customer = payload.get("customer") or {}
    cart = payload.get("cart") or []

    email = str(customer.get("email", "")).strip()
    name = str(customer.get("name", "")).strip()
    if not name or "@" not in email:
        return jsonify(error="Please provide a valid name and email."), 400
    if not isinstance(cart, list) or not cart:
        return jsonify(error="Your cart is empty."), 400

    total = Decimal("0")
    normalized_cart = []
    for item in cart:
        product = PRODUCT_BY_ID.get(str(item.get("id", "")))
        try:
            quantity = int(item.get("quantity", 0))
        except (TypeError, ValueError):
            quantity = 0
        if product is None or quantity < 1 or quantity > 20:
            return jsonify(error="One of the cart items is invalid."), 400
        total += Decimal(str(product["price"])) * quantity
        normalized_cart.append({"id": product["id"], "quantity": quantity})

    shipping = Decimal("0") if total >= Decimal("35") else Decimal("4.95")
    return jsonify(
        status="confirmed",
        order_id=f"BDK-{token_hex(3).upper()}",
        items=normalized_cart,
        subtotal=f"{total:.2f}",
        shipping=f"{shipping:.2f}",
        total=f"{total + shipping:.2f}",
    )


@app.after_request
def add_response_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if request.path.startswith(("/assets/", "/css/", "/js/")):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
