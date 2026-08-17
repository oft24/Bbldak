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
        "sku": "811140",
        "tagline": "Cremosa, picante y con final de queso.",
        "description": "Salsa de pollo picante con leche, mantequilla, mozzarella y pimienta negra.",
        "price": 2.49,
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
        "prepared_image": "/assets/prepared-carbonara.webp?v=1",
        "prepared_alt": "Buldak Carbonara preparada en un tazón junto a su paquete rosa",
        "prepared_source": "Modern Asia Market",
        "prepared_source_url": "https://mam-shop.at/products/samyang-buldak-carbonara-hot-chicken-ramen-130g",
        "recommendations": [
            {"title": "Huevo suave", "text": "La yema refuerza la textura cremosa sin ocultar el chile."},
            {"title": "Cebollín y hongos", "text": "Aportan frescura y umami a la salsa de queso."},
            {"title": "Pepino frío", "text": "Un acompañamiento crujiente y ácido limpia el paladar."},
        ],
        "nutrition_source_url": "https://www.samyangfoods.com/eng/brand/view.do?seq=399",
        "image": "/assets/carbonara.png?v=1",
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
        "id": "original",
        "number": "02",
        "name": "Original",
        "sku": "811120",
        "tagline": "El clásico: chile directo y final tostado.",
        "description": "Salsa de pollo picante, chile rojo, sésamo y alga tostada sin una capa láctea.",
        "price": 2.29,
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
        "prepared_image": "/assets/prepared-original.jpg?v=1",
        "prepared_alt": "Buldak Original preparada en sartén junto a su paquete negro",
        "prepared_source": "Tesco",
        "prepared_source_url": "https://www.tesco.com/groceries/en-GB/products/301413443",
        "recommendations": [
            {"title": "Huevo frito", "text": "La yema redondea el picor y añade cuerpo al fideo."},
            {"title": "Alga y cebollín", "text": "Refuerzan el acabado tostado y aportan frescura."},
            {"title": "Bebida láctea fría", "text": "La grasa láctea ayuda a bajar la sensación de capsaicina."},
        ],
        "nutrition_source_url": "https://www.samyangfoods.com/eng/brand/view.do?seq=245",
        "image": "/assets/original.png?v=1",
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
        "id": "quattro",
        "number": "03",
        "name": "Quattro Cheese",
        "sku": "811150",
        "tagline": "Cuatro quesos, salsa espesa y picor tardío.",
        "description": "Mozzarella, cheddar, gouda y camembert sobre la salsa Buldak picante.",
        "price": 2.79,
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
        "prepared_image": "/assets/prepared-quattro.webp?v=1",
        "prepared_alt": "Buldak Quattro Cheese preparada con queso fundido en un tazón amarillo",
        "prepared_source": "Yami",
        "prepared_source_url": "https://www.yami.com/en/p/buldak-quattro-cheese-hot-chicken-flavor-stir-fried-ramen-5-pack-x-4-76oz/1021096141",
        "recommendations": [
            {"title": "Maíz dorado", "text": "Su dulzor equilibra el chile y combina con los cuatro quesos."},
            {"title": "Pollo a la plancha", "text": "Añade proteína sin competir con la salsa cremosa."},
            {"title": "Pepinillos crujientes", "text": "La acidez corta la grasa y refresca entre bocados."},
        ],
        "nutrition_source_url": "https://samyangamerica.com/buldak/quattro-cheese",
        "image": "/assets/quattro.png?v=1",
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

PRODUCT_BY_ID = {product["id"]: product for product in PRODUCTS}
PRODUCT_ASSET_DIR = Path(__file__).resolve().parent / "assets"


@app.get("/")
def index():
    return render_template("index.html", products=PRODUCTS)


@app.get("/api/health")
def health():
    return jsonify(status="ok", service="buldakshop")


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
        return jsonify(error="Ingresa un nombre y un correo válidos."), 400
    if not isinstance(cart, list) or not cart:
        return jsonify(error="Tu carrito está vacío."), 400

    total = Decimal("0")
    normalized_cart = []
    for item in cart:
        product = PRODUCT_BY_ID.get(str(item.get("id", "")))
        try:
            quantity = int(item.get("quantity", 0))
        except (TypeError, ValueError):
            quantity = 0
        if product is None or quantity < 1 or quantity > 20:
            return jsonify(error="Uno de los artículos del carrito no es válido."), 400
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
