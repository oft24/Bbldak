from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from secrets import token_hex

from flask import Flask, jsonify, render_template, request, send_from_directory

from backend.supabase_repository import ProductRepository

ROOT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT_DIR / "frontend"
app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR / "static"),
    static_url_path="",
    template_folder=str(FRONTEND_DIR / "templates"),
)


PRODUCTS = [
    {
        "id": "811140",
        "number": "01",
        "name": "Carbonara",
        "sku": "811140",
        "tagline": "Cremosa, picante y con final de queso.",
        "description": "Salsa de pollo picante con leche, mantequilla, mozzarella y pimienta negra.",
        "price": 0.01,
        "price_label": "$0.01",
        "weight": "130 g · paquete individual",
        "heat": 40,
        "heat_label": "Picor cremoso · 2/5",
        "shu": "2,600",
        "kcal": "550",
        "cook_time": "5 min",
        "story_title": ["Cremosa.", "Picante.", "Muy Carbonara."],
        "story": (
            "La bolsa rosa mezcla la salsa Buldak con un polvo de queso y crema. "
            "Primero llega la mozzarella y la mantequilla; después aparecen el chile, "
            "el ajo y la pimienta negra. Es una porción de 130 g con 550 kcal."
        ),
        "story_note": "Queso primero.\nPicor después.",
        "ingredients": ["Mozzarella", "Leche", "Chile", "Pimienta"],
        "ingredient_intro": "Cuatro notas que explican el sabor de Carbonara.",
        "profile": [
            {"label": "Entrada", "value": "Leche y mantequilla"},
            {"label": "Centro", "value": "Mozzarella y salsa Buldak"},
            {"label": "Final", "value": "Chile, ajo y pimienta negra"},
        ],
        "allergens": "Contiene trigo, soya y leche.",
        "directions_title": ["Cinco minutos.", "Cremosidad exacta."],
        "directions_intro": "Preparación para la bolsa Carbonara de 130 g.",
        "directions": [
            {"title": "Hierve", "text": "Lleva 600 ml de agua a ebullición."},
            {"title": "Cocina", "text": "Añade los fideos y cocina durante 5 minutos."},
            {"title": "Reserva", "text": "Escurre, dejando 8 cucharadas (aprox. 120 ml) de agua."},
            {"title": "Mezcla", "text": "Agrega la salsa y el polvo de queso; mezcla bien y sirve."},
        ],
        "prepared_image": "/assets/prepared-carbonara.jpg?v=3",
        "prepared_alt": "Buldak Carbonara preparada en un tazón junto a su paquete rosa",
        "prepared_source": "Buldak.com",
        "prepared_source_url": "https://buldak.com/us/product/buldak-ramen-carbonara/",
        "recommendations": [
            {"title": "Huevo suave", "text": "La yema refuerza la textura cremosa sin ocultar el chile."},
            {"title": "Cebollín y hongos", "text": "Aportan frescura y umami a la salsa de queso."},
            {"title": "Pepino frío", "text": "Un acompañamiento crujiente y ácido limpia el paladar."},
        ],
        "nutrition_source_url": "https://www.samyangfoods.com/eng/brand/view.do?seq=399",
        "image": "/assets/carbonara.png?v=3",
        "colors": {
            "bg_a": "#f5d9e1",
            "bg_b": "#fff8f4",
            "glow": "#ffc1d2",
            "ink": "#2b171e",
            "accent": "#b3123f",
        },
        "keywords": "carbonara carbo cremosa crema suave queso rosa mozzarella",
    },
    {
        "id": "811120",
        "number": "02",
        "name": "Original",
        "sku": "811120",
        "tagline": "El clásico: chile directo y final tostado.",
        "description": "Salsa de pollo picante, chile rojo, sésamo y alga tostada sin una capa láctea.",
        "price": 0.01,
        "price_label": "$0.01",
        "weight": "140 g · paquete individual",
        "heat": 82,
        "heat_label": "Muy picante · 5/5",
        "shu": "4,404",
        "kcal": "530",
        "cook_time": "5 min",
        "story_title": ["Directa.", "Tostada.", "La original."],
        "story": (
            "La bolsa negra es la receta que inició el reto Buldak. La salsa se adhiere "
            "al fideo sin caldo: primero se siente el pollo especiado y el curry; luego "
            "sube el chile, con sésamo y alga tostada al final."
        ),
        "story_note": "Sin caldo.\nPicor frontal.",
        "ingredients": ["Chile rojo", "Sésamo", "Alga tostada", "Ajo"],
        "ingredient_intro": "Los elementos que forman el perfil seco y tostado de Original.",
        "profile": [
            {"label": "Entrada", "value": "Pollo especiado y curry"},
            {"label": "Centro", "value": "Chile rojo y ajo"},
            {"label": "Final", "value": "Sésamo y alga tostada"},
        ],
        "allergens": "Contiene trigo, soya y sésamo.",
        "directions_title": ["Cinco minutos.", "Treinta segundos al fuego."],
        "directions_intro": "Preparación para la bolsa Original de 140 g.",
        "directions": [
            {"title": "Hierve", "text": "Lleva 600 ml de agua a ebullición."},
            {"title": "Cocina", "text": "Añade los fideos y cocina durante 5 minutos."},
            {"title": "Reserva", "text": "Escurre, dejando 1/2 taza (aprox. 120 ml) de agua."},
            {"title": "Saltea", "text": "Añade la salsa, saltea 30 segundos y termina con las hojuelas."},
        ],
        "prepared_image": "/assets/prepared-original.webp?v=3",
        "prepared_alt": "Buldak Original preparada en sartén junto a su paquete negro",
        "prepared_source": "Buldak.com",
        "prepared_source_url": "https://buldak.com/us/product/buldak-ramen-original/",
        "recommendations": [
            {"title": "Huevo frito", "text": "La yema redondea el picor y añade cuerpo al fideo."},
            {"title": "Alga y cebollín", "text": "Refuerzan el acabado tostado y aportan frescura."},
            {"title": "Bebida láctea fría", "text": "La grasa láctea ayuda a bajar la sensación de capsaicina."},
        ],
        "nutrition_source_url": "https://www.samyangfoods.com/eng/brand/view.do?seq=245",
        "image": "/assets/original.png?v=3",
        "colors": {
            "bg_a": "#120e0d",
            "bg_b": "#2a110b",
            "glow": "#ff642f",
            "ink": "#f8f2ef",
            "accent": "#ff5a20",
        },
        "keywords": "original picante fuego clásico negra chile sésamo alga",
    },
    {
        "id": "811150",
        "number": "03",
        "name": "Quattro Cheese",
        "sku": "811150",
        "tagline": "Cuatro quesos, salsa espesa y picor tardío.",
        "description": "Mozzarella, cheddar, gouda y camembert sobre la salsa Buldak picante.",
        "price": 0.01,
        "price_label": "$0.01",
        "weight": "145 g · paquete individual",
        "heat": 60,
        "heat_label": "Picante con queso · 3/5",
        "shu": "≈2,323",
        "kcal": "590",
        "cook_time": "5 min 30 s",
        "story_title": ["Cuatro quesos.", "Una salsa.", "Picor tardío."],
        "story": (
            "Mozzarella, cheddar, gouda y camembert forman una salsa densa y salada. "
            "La primera impresión es láctea; el chile aparece después y se queda en el "
            "paladar. La bolsa del catálogo contiene 145 g."
        ),
        "story_note": "Cuatro quesos.\nUn final picante.",
        "ingredients": ["Mozzarella", "Cheddar", "Gouda", "Camembert"],
        "ingredient_intro": "Los cuatro quesos declarados para Quattro Cheese.",
        "profile": [
            {"label": "Entrada", "value": "Mozzarella cremosa"},
            {"label": "Centro", "value": "Cheddar y gouda salados"},
            {"label": "Final", "value": "Camembert, ajo y chile"},
        ],
        "allergens": "Contiene trigo, soya y leche.",
        "directions_title": ["Cinco y medio.", "Todo el queso."],
        "directions_intro": "Preparación para la bolsa Quattro Cheese de 145 g.",
        "directions": [
            {"title": "Hierve", "text": "Lleva 600 ml de agua a ebullición."},
            {"title": "Cocina", "text": "Añade los fideos y cocina 5 minutos con 30 segundos."},
            {"title": "Reserva", "text": "Escurre, dejando 6 cucharadas (aprox. 90 ml) de agua."},
            {"title": "Mezcla", "text": "Añade la salsa y el polvo de cuatro quesos; mezcla y sirve."},
        ],
        "prepared_image": "/assets/prepared-quattro.jpg?v=3",
        "prepared_alt": "Buldak Quattro Cheese preparada con queso fundido en un tazón amarillo",
        "prepared_source": "Buldak.com",
        "prepared_source_url": "https://buldak.com/us/product/buldak-ramen-quattro-cheese/",
        "recommendations": [
            {"title": "Maíz dorado", "text": "Su dulzor equilibra el chile y combina con los cuatro quesos."},
            {"title": "Pollo a la plancha", "text": "Añade proteína sin competir con la salsa cremosa."},
            {"title": "Pepinillos crujientes", "text": "La acidez corta la grasa y refresca entre bocados."},
        ],
        "nutrition_source_url": "https://samyangamerica.com/buldak/quattro-cheese",
        "image": "/assets/quattro.png?v=3",
        "colors": {
            "bg_a": "#f3c45d",
            "bg_b": "#fff2d6",
            "glow": "#ffde8f",
            "ink": "#392608",
            "accent": "#b64b0c",
        },
        "keywords": "quattro cuatro quesos mozzarella cheddar gouda camembert amarilla",
    },
]

CATALOG_CATEGORIES = [
    {"id": "all", "label": "Todos"},
    {"id": "bags", "label": "Bolsas"},
    {"id": "bowls", "label": "Bowls"},
    {"id": "tteokbokki", "label": "Tteokbokki"},
    {"id": "snacks", "label": "Snacks"},
]


CATALOG_PRODUCTS = [
    {
        "sku": "811140", "name": "Carbonara", "category": "bags", "category_label": "Bolsa",
        "weight": "130 g", "case": "40 paquetes", "image": "/assets/carbonara.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-carbonara/", "status": "Disponible",
    },
    {
        "sku": "811130", "name": "Cream Carbonara", "category": "bags", "category_label": "Bolsa",
        "weight": "140 g", "case": "40 paquetes", "image": "/assets/catalog/cream-carbonara.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-cream-carbonara/", "status": "Disponible",
    },
    {
        "sku": "811200", "name": "Cheese", "category": "bags", "category_label": "Bolsa",
        "weight": "140 g", "case": "40 paquetes", "image": "/assets/catalog/cheese.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-cheese/", "status": "Disponible",
    },
    {
        "sku": "811150", "name": "Quattro Cheese", "category": "bags", "category_label": "Bolsa",
        "weight": "145 g", "case": "40 paquetes", "image": "/assets/quattro.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-quattro-cheese/", "status": "Disponible",
    },
    {
        "sku": "811270", "name": "Rosé", "category": "bags", "category_label": "Bolsa",
        "weight": "140 g", "case": "40 paquetes", "image": "/assets/catalog/rose.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-rose/", "status": "Disponible",
    },
    {
        "sku": "811320", "name": "Sweet & Spicy", "category": "bags", "category_label": "Bolsa",
        "weight": "140 g", "case": "40 paquetes", "image": "/assets/catalog/sweet-spicy.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-swicy/", "status": "Disponible",
    },
    {
        "sku": "811000", "name": "Taco", "category": "bags", "category_label": "Bolsa",
        "weight": "140 g", "case": "40 paquetes", "image": "/assets/catalog/taco.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-taco/", "status": "Disponible",
    },
    {
        "sku": "811340", "name": "Yakisoba", "category": "bags", "category_label": "Bolsa",
        "weight": "150 g", "case": "40 paquetes", "image": "/assets/catalog/yakisoba.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-yakisoba/", "status": "Disponible",
    },
    {
        "sku": "811220", "name": "Habanero Lime", "category": "bags", "category_label": "Bolsa",
        "weight": "135 g", "case": "40 paquetes", "image": "/assets/catalog/habanero-lime.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-habanero-lime/", "status": "Disponible",
    },
    {
        "sku": "811120", "name": "Original", "category": "bags", "category_label": "Bolsa",
        "weight": "140 g", "case": "40 paquetes", "image": "/assets/original.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-original/", "status": "Disponible",
    },
    {
        "sku": "811210", "name": "2X Spicy", "category": "bags", "category_label": "Bolsa",
        "weight": "140 g", "case": "40 paquetes", "image": "/assets/catalog/2x-spicy.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-2x/", "status": "Disponible",
    },
    {
        "sku": "811616", "name": "Sweet & Spicy Korean Chicken", "category": "bowls", "category_label": "Big Bowl",
        "weight": "115 g", "case": "6 bowls", "image": "/assets/catalog/sweet-spicy-bowl.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-swicy-big-bowl/", "status": "Disponible",
    },
    {
        "sku": "811618", "name": "Quattro Cheese Big Bowl", "category": "bowls", "category_label": "Big Bowl",
        "weight": "110 g", "case": "6 bowls", "image": "/assets/catalog/quattro-bowl.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-quattro-cheese-big-bowl/", "status": "Disponible",
    },
    {
        "sku": "811622", "name": "Carbonara Big Bowl", "category": "bowls", "category_label": "Big Bowl",
        "weight": "105 g", "case": "6 bowls", "image": "/assets/catalog/carbonara-bowl.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-carbonara-big-bowl/", "status": "Disponible",
    },
    {
        "sku": "811624", "name": "Original Big Bowl", "category": "bowls", "category_label": "Big Bowl",
        "weight": "105 g", "case": "6 bowls", "image": "/assets/catalog/original-bowl.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-original-big-bowl/", "status": "Disponible",
    },
    {
        "sku": "811640", "name": "Rosé Big Bowl", "category": "bowls", "category_label": "Big Bowl",
        "weight": "105 g", "case": "6 bowls", "image": "/assets/catalog/rose-bowl.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-rose-big-bowl/", "status": "Disponible",
    },
    {
        "sku": "811650", "name": "Rosé Wide Glass Noodle", "category": "bowls", "category_label": "Wide Glass Noodle",
        "weight": "169.4 g", "case": "16 bowls", "image": "/assets/catalog/wide-glass-noodle.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-wide-glass-noodle-rose-169-4g/", "status": "Disponible",
    },
    {
        "sku": "811612", "name": "Original Big Bowl", "category": "bowls", "category_label": "Big Bowl · SKU alterno",
        "weight": "105 g", "case": "6 bowls", "image": "/assets/catalog/original-bowl.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-ramen-original-big-bowl/", "status": "Disponible",
    },
    {
        "sku": "811710", "name": "Carbonara Tteokbokki", "category": "tteokbokki", "category_label": "Tteokbokki",
        "weight": "179 g", "case": "16 bowls", "image": "/assets/catalog/carbonara-tteokbokki.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-carbonara-tteokbokki-179g/", "status": "Disponible",
    },
    {
        "sku": "811720", "name": "Original Tteokbokki", "category": "tteokbokki", "category_label": "Tteokbokki",
        "weight": "179 g", "case": "16 bowls", "image": "/assets/catalog/original-tteokbokki.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-tteokbokki-185g/", "status": "Agotado · 14 jul 2026",
    },
    {
        "sku": "811910", "name": "Potato Chips Habanero Lime", "category": "snacks", "category_label": "Snack",
        "weight": "120 g", "case": "12 bolsas", "image": "/assets/catalog/chips-habanero.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-potato-chips-habanero-lime-120g/", "status": "Disponible",
    },
    {
        "sku": "811920", "name": "Potato Chips Original", "category": "snacks", "category_label": "Snack",
        "weight": "120 g", "case": "12 bolsas", "image": "/assets/catalog/chips-original.png?v=3",
        "source_url": "https://buldak.com/us/product/buldak-potato-chips-original-120g/", "status": "Disponible",
    },
]


for sort_order, catalog_product in enumerate(CATALOG_PRODUCTS, start=1):
    catalog_product.update(
        id=catalog_product["sku"],
        price=0.01,
        price_label="$0.01",
        sort_order=sort_order,
        is_available=not catalog_product["status"].startswith("Agotado"),
    )

PRODUCT_ASSET_DIR = FRONTEND_DIR / "assets"
repository = ProductRepository()


def current_catalog() -> list[dict]:
    """Return Supabase products, preserving a local fallback for development."""
    return repository.list_products(CATALOG_PRODUCTS)


def carousel_catalog(catalog_products: list[dict]) -> list[dict]:
    """Keep ramen first, bowls in the middle, and snacks at the end."""
    lead_ids = ("811120", "811140", "811150")
    product_by_id = {str(product["id"]): product for product in catalog_products}
    lead = [product_by_id[product_id] for product_id in lead_ids if product_id in product_by_id]
    lead_set = set(lead_ids)
    remainder = [product for product in catalog_products if str(product["id"]) not in lead_set]
    category_order = {"bags": 0, "bowls": 1, "tteokbokki": 2, "snacks": 3}
    remainder.sort(
        key=lambda product: (
            category_order.get(product.get("category", ""), 4),
            product.get("sort_order", 999),
        )
    )
    return [*lead, *remainder]


@app.get("/")
def index():
    catalog_products = current_catalog()
    return render_template(
        "index.html",
        products=PRODUCTS,
        catalog_products=catalog_products,
        carousel_products=carousel_catalog(catalog_products),
        catalog_categories=CATALOG_CATEGORIES,
    )


@app.get("/api/health")
def health():
    return jsonify(
        status="ok",
        service="buldakshop",
        database="supabase" if repository.is_configured else "local-fallback",
        catalog_source=repository.last_source,
    )


@app.get("/api/products")
def products():
    return jsonify(products=PRODUCTS)


@app.get("/api/catalog")
def catalog():
    return jsonify(products=current_catalog(), source=repository.last_source)


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
        return jsonify(error="Ingresa un nombre y un correo válidos."), 400
    if not isinstance(cart, list) or not cart:
        return jsonify(error="Tu carrito está vacío."), 400
    catalog_by_id = {product["id"]: product for product in current_catalog()}
    total = Decimal("0")
    normalized_cart = []
    for item in cart:
        product = catalog_by_id.get(str(item.get("id", "")))
        try:
            quantity = int(item.get("quantity", 0))
        except (TypeError, ValueError):
            quantity = 0
        if product is None or quantity < 1 or quantity > 20 or not product.get("is_available", True):
            return jsonify(error="Uno de los artículos del carrito no es válido."), 400
        total += Decimal(str(product["price"])) * quantity
        normalized_cart.append({"id": product["id"], "quantity": quantity})

    shipping = Decimal("0")
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
