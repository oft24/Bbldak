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


# Wholesale packing taken from the July Buldak price list: how many retail units
# travel inside one case, the size of each unit, and the price of that case.
# (units, unit_size, case_price, unit_noun)
BULDAK_PACKS = {
    "811140": (40, "130 g", 1120, "paquetes"),
    "811130": (40, "140 g", 1120, "paquetes"),
    "811200": (40, "140 g", 1120, "paquetes"),
    "811150": (40, "145 g", 1120, "paquetes"),
    "811270": (40, "140 g", 1120, "paquetes"),
    "811320": (40, "140 g", 1120, "paquetes"),
    "811000": (40, "140 g", 1120, "paquetes"),
    "811340": (40, "150 g", 1120, "paquetes"),
    "811220": (40, "135 g", 1120, "paquetes"),
    "811120": (40, "140 g", 1120, "paquetes"),
    "811210": (40, "140 g", 1120, "paquetes"),
    "811616": (6, "115 g", 340, "bowls grandes"),
    "811618": (6, "110 g", 340, "bowls grandes"),
    "811622": (6, "105 g", 340, "bowls grandes"),
    "811624": (6, "105 g", 340, "bowls grandes"),
    "811640": (6, "105 g", 340, "bowls grandes"),
    "811612": (6, "105 g", 290, "bowls grandes"),
    "811650": (16, "169.4 g", 1050, "bowls"),
    "811710": (16, "179 g", 1375, "bowls"),
    "811720": (16, "179 g", 1375, "bowls"),
    "811910": (12, "120 g", 900, "bolsas"),
    "811920": (12, "120 g", 900, "bolsas"),
}


def apply_pack(product, units, unit_size, case_price, unit_noun, inner=None, promo=None):
    """Attach the wholesale case model every product is sold by."""
    if inner:
        outer = units // inner
        pack_label = f"{outer} paquetes de {inner} {unit_noun} de {unit_size}"
    else:
        pack_label = f"{units} {unit_noun} de {unit_size}"
    product.update(
        units_per_case=units,
        unit_size=unit_size,
        unit_noun=unit_noun,
        inner_packs=inner,
        pack_label=pack_label,
        pack_short=f"{units} {unit_noun}",
        case_total=f"{units} × {unit_size}",
        promo=promo,
        price=float(case_price),
        price_label=f"${case_price:,.0f}",
        unit_price_label=f"${case_price / units:,.2f}",
    )
    return product


# Market names for every SKU: the English name the maker exports under and the
# Japanese name it is sold as. Buldak follows Samyang Japan's "<sabor>ブルダック炒め麺".
INTL_NAMES = {
    # --- Buldak ---
    "811140": ("Carbonara Buldak Stir-Fried Ramen", "カルボナーラブルダック炒め麺"),
    "811130": ("Cream Carbonara Buldak Stir-Fried Ramen", "クリームカルボナーラブルダック炒め麺"),
    "811200": ("Cheese Buldak Stir-Fried Ramen", "チーズブルダック炒め麺"),
    "811150": ("Quattro Cheese Buldak Stir-Fried Ramen", "クアトロチーズブルダック炒め麺"),
    "811270": ("Rosé Buldak Stir-Fried Ramen", "ロゼブルダック炒め麺"),
    "811320": ("Swicy Buldak Stir-Fried Ramen", "スワイシーブルダック炒め麺"),
    "811000": ("Taco Buldak Stir-Fried Ramen", "タコブルダック炒め麺"),
    "811340": ("Yakisoba Buldak Stir-Fried Ramen", "焼きそばブルダック炒め麺"),
    "811220": ("Habanero Lime Buldak Stir-Fried Ramen", "ハバネロライムブルダック炒め麺"),
    "811120": ("Original Buldak Stir-Fried Ramen", "ブルダック炒め麺"),
    "811210": ("2X Spicy Buldak Stir-Fried Ramen", "2倍辛ブルダック炒め麺"),
    "811616": ("Swicy Buldak Stir-Fried Ramen Big Bowl", "スワイシーブルダック炒め麺 BIG"),
    "811618": ("Quattro Cheese Buldak Stir-Fried Ramen Big Bowl", "クアトロチーズブルダック炒め麺 BIG"),
    "811622": ("Carbonara Buldak Stir-Fried Ramen Big Bowl", "カルボナーラブルダック炒め麺 BIG"),
    "811624": ("Original Buldak Stir-Fried Ramen Big Bowl", "ブルダック炒め麺 BIG"),
    "811640": ("Rosé Buldak Stir-Fried Ramen Big Bowl", "ロゼブルダック炒め麺 BIG"),
    "811650": ("Rosé Buldak Wide Glass Noodle", "ロゼブルダック太春雨"),
    "811612": ("Original Buldak Stir-Fried Ramen Big Bowl", "ブルダック炒め麺 BIG"),
    "811710": ("Carbonara Buldak Tteokbokki", "カルボナーラブルダックトッポギ"),
    "811720": ("Original Buldak Tteokbokki", "ブルダックトッポギ"),
    "811910": ("Buldak Potato Chips Habanero Lime", "ブルダックポテトチップス ハバネロライム"),
    "811920": ("Buldak Potato Chips Original", "ブルダックポテトチップス オリジナル"),
    # --- Refrescos ---
    "833130": ("Coconut Palm Coconut Juice", "椰樹 ココナッツジュース"),
    "833210": ("Wong Lo Kat Herbal Tea", "王老吉 漢方茶"),
    "831190": ("Chi Forest Sparkling Water White Peach", "元気森林 スパークリングウォーター 白桃"),
    "194280": ("Vita Peach Tea", "ビタ ピーチティー"),
    "880350": ("Binggrae Melon Flavored Milk", "ビングレ メロン牛乳"),
    "831214": ("Chi Forest Sparkling Water Lemon Cola", "元気森林 スパークリングウォーター レモンコーラ"),
    "834510": ("Shuiquanwan Lactic Acid Yogurt Drink", "水泉湾 乳酸菌飲料"),
    "832110": ("Master Kong Jasmine Green Tea", "康師傅 ジャスミン緑茶"),
    "832160": ("Master Kong Rock Sugar Pear Drink", "康師傅 氷糖雪梨"),
    "832140": ("Master Kong Honey Pomelo Tea", "康師傅 蜂蜜柚子茶"),
    "831831": ("Hawthorn Juice and Pulp Drink", "山楂樹下 サンザシドリンク"),
    "837410": ("Tea 365 Green Tea Lemon & Lemongrass", "緑茶365 レモン&レモングラス"),
    "837412": ("Tea 365 Green Tea Honey", "緑茶365 ハニー"),
    "831160": ("Chi Forest Sparkling Water Lychee", "元気森林 スパークリングウォーター ライチ"),
    "831220": ("Chi Forest Sparkling Water White Peach Can", "元気森林 スパークリングウォーター 白桃 缶"),
    "831170": ("Chi Forest Sparkling Water Grape Delight", "元気森林 スパークリングウォーター ブドウ"),
    "831140": ("Chi Forest Sparkling Water Orange Vitamin C", "元気森林 スパークリングウォーター オレンジ"),
    "831240": ("Chi Forest Sparkling Water Lychee Can", "元気森林 スパークリングウォーター ライチ 缶"),
    "833320": ("Taisun Grass Jelly Drink Original", "泰山 仙草蜜ドリンク オリジナル"),
    "833330": ("Taisun Grass Jelly Drink Lychee", "泰山 仙草蜜ドリンク ライチ"),
    "833340": ("Taisun Grass Jelly Drink Coconut", "泰山 仙草蜜ドリンク ココナッツ"),
    "837520": ("J WAY Instant Boba Fruit Juice Kit", "J WAY タピオカ フルーツジュースキット"),
    "837510": ("J WAY Instant Boba Milk Tea Kit", "J WAY タピオカ ミルクティーキット"),
    "838210": ("Dongpeng Water Boost Electrolyte Drink Lemon", "東鵬 補水啦 電解質ドリンク レモン"),
    "838212": ("Dongpeng Water Boost Electrolyte Drink Grapefruit", "東鵬 補水啦 電解質ドリンク グレープフルーツ"),
    "838214": ("Dongpeng Water Boost Electrolyte Drink Lychee", "東鵬 補水啦 電解質ドリンク ライチ"),
    "838312": ("Dongpeng Water Boost Electrolyte Drink Lemon 555 ml", "東鵬 補水啦 電解質ドリンク レモン 555ml"),
    "838314": ("Dongpeng Water Boost Electrolyte Drink Lychee 555 ml", "東鵬 補水啦 電解質ドリンク ライチ 555ml"),
    "838310": ("Dongpeng Water Boost Electrolyte Drink Grapefruit 555 ml", "東鵬 補水啦 電解質ドリンク グレープフルーツ 555ml"),
    "880910": ("Haitai Grape Bongbong Juice", "ヘテ ぶどうボンボン"),
    "880010": ("Yogo Vera Aloe Vera Drink Mango", "ヨゴベラ アロエドリンク マンゴー"),
    "880020": ("Yogo Vera Aloe Vera Drink Mango 1.5 L", "ヨゴベラ アロエドリンク マンゴー 1.5L"),
    "880030": ("Yogo Vera Aloe Vera Drink Strawberry", "ヨゴベラ アロエドリンク いちご"),
    "880040": ("Yogo Vera Aloe Vera Drink Peach 1.5 L", "ヨゴベラ アロエドリンク 白桃 1.5L"),
    "831390": ("Ramune Soda Strawberry", "ラムネ いちご"),
    "831410": ("Ramune Soda Original", "ラムネ オリジナル"),
    "880600": ("Tomomasu Watermelon Soda", "友桝飲料 スイカサイダー"),
    "880604": ("Tomomasu White Peach Soda", "友桝飲料 白桃サイダー"),
    "880602": ("Tomomasu Mango Soda", "友桝飲料 マンゴーサイダー"),
}


def apply_intl_names(product):
    """Attach the English and Japanese market names to one product."""
    name_en, name_ja = INTL_NAMES.get(product["sku"], (product["name"], ""))
    product["name_en"] = name_en
    product["name_ja"] = name_ja
    return product


for sort_order, catalog_product in enumerate(CATALOG_PRODUCTS, start=1):
    units, unit_size, case_price, unit_noun = BULDAK_PACKS[catalog_product["sku"]]
    catalog_product.update(
        id=catalog_product["sku"],
        sort_order=sort_order,
        is_available=not catalog_product["status"].startswith("Agotado"),
    )
    apply_pack(catalog_product, units, unit_size, case_price, unit_noun)
    apply_intl_names(catalog_product)
    catalog_product["case"] = catalog_product["pack_label"]


REFRESCOS_CATEGORIES = [
    {"id": "all", "label": "Todos"},
    {"id": "te", "label": "Té"},
    {"id": "agua_gas", "label": "Agua con gas"},
    {"id": "jugos_lacteos", "label": "Jugos y lácteos"},
    {"id": "electrolitos", "label": "Electrolitos"},
    {"id": "boba", "label": "Boba"},
    {"id": "otros", "label": "Otros"},
]

_REFRESCOS_CATEGORY_LABELS = {c["id"]: c["label"] for c in REFRESCOS_CATEGORIES}


def _refresco(sku, name, category, image, description, units, unit_size, case_price,
              unit_noun="botellas", inner=None, promo=None):
    """One wholesale line from the Catalogo 0908 drinks pages."""
    product = {
        "sku": sku, "id": sku, "name": name, "category": category,
        "category_label": _REFRESCOS_CATEGORY_LABELS[category],
        "weight": f"{unit_size} · {unit_noun.rstrip('es').rstrip('s')}",
        "image": f"/assets/refrescos/{image}.webp?v=2",
        "description": description, "status": "Disponible",
    }
    apply_pack(product, units, unit_size, case_price, unit_noun, inner=inner, promo=promo)
    product["case"] = product["pack_label"]
    return product


# Promotions printed in the source catalog (买十送一 / 买五送二).
BUY_10_GET_1 = "promo.buy10get1"
BUY_5_GET_2 = "promo.buy5get2"


REFRESCOS_PRODUCTS = [
    _refresco("833130", "Coco Palm Jugo de Coco", "jugos_lacteos", "833130",
        "Jugo de coco 100% natural en lata, ligero, dulce y sin pulpa.",
        24, "245 ml", 650, "latas"),
    _refresco("833210", "Wang Lo Kat Té de Hierbas", "otros", "833210",
        "Bebida herbal china clásica (凉茶), dulce y refrescante, ideal para acompañar comidas picantes.",
        24, "310 ml", 450, "latas"),
    _refresco("831190", "Genki Forest Soda Durazno Blanco", "agua_gas", "831190",
        "Agua con gas sabor durazno blanco, cero azúcar, ligera y burbujeante.",
        15, "480 ml", 435),
    _refresco("194280", "Vita Té de Durazno", "te", "194280",
        "Té de durazno clásico, dulce y ligero, listo para tomar frío.",
        48, "250 ml", 850),
    _refresco("880350", "Binggrae Leche Sabor Melón", "jugos_lacteos", "880350",
        "Bebida láctea coreana con sabor a melón, cremosa y dulce.",
        24, "200 ml", 650),
    _refresco("831214", "Genki Forest Cola Limón Gasificada", "agua_gas", "831214",
        "Agua con gas sabor cola y limón, cero azúcar.",
        15, "480 ml", 425),
    _refresco("834510", "Shui Lian Wan Yogurt Original", "jugos_lacteos", "834510",
        "Bebida con sabor a yogurt, cremosa y ligeramente dulce.",
        20, "280 ml", 750),
    _refresco("832110", "Kang Shi Fu Té de Jazmín", "te", "832110",
        "Té verde con jazmín en botella verde, refrescante y floral.",
        15, "500 ml", 255),
    _refresco("832160", "Kang Shi Fu Pera con Azúcar de Roca", "te", "832160",
        "Té de pera con azúcar de roca, suave y ligeramente dulce.",
        15, "500 ml", 255),
    _refresco("832140", "Kang Shi Fu Té de Toronja con Miel", "te", "832140",
        "Té de toronja (pomelo) con miel, cítrico y dulce.",
        15, "500 ml", 255),
    _refresco("831831", "Shan Zha Shu Xia Bebida de Espino", "otros", "831831",
        "Bebida de espino (shanzha) agridulce, un clásico chino digestivo.",
        15, "350 ml", 600, promo=BUY_5_GET_2),
    _refresco("837410", "MASAN Té Verde Limón y Limoncillo", "te", "837410",
        "Té verde con limón y limoncillo, fresco y aromático.",
        24, "500 ml", 385),
    _refresco("837412", "MASAN Té Verde con Miel", "te", "837412",
        "Té verde suave endulzado con miel.",
        24, "500 ml", 385),
    _refresco("831160", "Genki Forest Soda Lichi", "agua_gas", "831160",
        "Agua con gas sabor lichi, cero azúcar, ligera y afrutada.",
        15, "480 ml", 435),
    _refresco("831220", "Genki Forest Soda Durazno Blanco Lata", "agua_gas", "831220",
        "Versión en lata del agua con gas sabor durazno blanco, cero azúcar.",
        24, "330 ml", 435, "latas", inner=6),
    _refresco("831170", "Genki Forest Soda Uva Negra de Verano", "agua_gas", "831170",
        "Agua con gas sabor uva negra, cero azúcar, dulce y burbujeante.",
        15, "480 ml", 369),
    _refresco("831140", "Genki Forest Soda Naranja con Vitamina C", "agua_gas", "831140",
        "Agua con gas sabor naranja con vitamina C, cero azúcar.",
        15, "480 ml", 435),
    _refresco("831240", "Genki Forest Soda Lichi Lata", "agua_gas", "831240",
        "Versión en lata del agua con gas sabor lichi, cero azúcar.",
        24, "330 ml", 475, "latas", inner=6),
    _refresco("833320", "Tai Shan Gelatina de Hierba Original", "otros", "833320",
        "Bebida de gelatina de hierba (仙草蜜), refrescante y ligeramente dulce.",
        24, "330 g", 510, "latas", inner=6),
    _refresco("833330", "Tai Shan Gelatina de Hierba Lichi", "otros", "833330",
        "Gelatina de hierba con sabor a lichi.",
        24, "330 g", 510, "latas", inner=6),
    _refresco("833340", "Tai Shan Gelatina de Hierba Coco", "otros", "833340",
        "Gelatina de hierba con sabor a coco.",
        24, "330 g", 510, "latas", inner=6),
    _refresco("837520", "J WAY Boba de Jugo de Fruta", "boba", "837520",
        "Kit de boba con jugo de fruta, 8 vasos individuales listos para preparar.",
        8, "125 g", 450, "vasos"),
    _refresco("837510", "J WAY Boba de Té con Leche", "boba", "837510",
        "Kit de boba de té con leche, 8 vasos individuales listos para preparar.",
        8, "78 g", 350, "vasos"),
    _refresco("838210", "Dongpeng Electrolitos Limón", "electrolitos", "838210",
        "Bebida electrolítica sabor limón para hidratación rápida.",
        12, "1000 ml", 415, promo=BUY_10_GET_1),
    _refresco("838212", "Dongpeng Electrolitos Toronja", "electrolitos", "838212",
        "Bebida electrolítica sabor toronja para hidratación rápida.",
        12, "1000 ml", 415, promo=BUY_10_GET_1),
    _refresco("838214", "Dongpeng Electrolitos Lichi", "electrolitos", "838214",
        "Bebida electrolítica sabor lichi para hidratación rápida.",
        12, "1000 ml", 415, promo=BUY_10_GET_1),
    _refresco("838312", "Dongpeng Electrolitos Limón 555 ml", "electrolitos", "838312",
        "Presentación de 555 ml de la bebida electrolítica sabor limón.",
        24, "555 ml", 575, promo=BUY_10_GET_1),
    _refresco("838314", "Dongpeng Electrolitos Lichi 555 ml", "electrolitos", "838314",
        "Presentación de 555 ml de la bebida electrolítica sabor lichi.",
        24, "555 ml", 575, promo=BUY_10_GET_1),
    _refresco("838310", "Dongpeng Electrolitos Toronja 555 ml", "electrolitos", "838310",
        "Presentación de 555 ml de la bebida electrolítica sabor toronja.",
        24, "555 ml", 575, promo=BUY_10_GET_1),
    _refresco("880910", "Haitai Jugo de Uva en Lata", "jugos_lacteos", "880910",
        "Jugo de uva coreano en lata, dulce y con trocitos de fruta (봉봉).",
        72, "238 ml", 1750, "latas", inner=12),
    _refresco("880010", "Yogo Bebida de Mango con Aloe", "jugos_lacteos", "880010",
        "Bebida de mango con trocitos de aloe vera.",
        20, "500 ml", 850),
    _refresco("880020", "Yogo Bebida de Mango con Aloe 1.5 L", "jugos_lacteos", "880020",
        "Presentación de 1.5 L de la bebida de mango con aloe vera.",
        12, "1.5 L", 1100),
    _refresco("880030", "Yogo Bebida de Fresa con Aloe", "jugos_lacteos", "880030",
        "Bebida de fresa con trocitos de aloe vera.",
        20, "500 ml", 850),
    _refresco("880040", "Yogo Bebida de Durazno con Aloe 1.5 L", "jugos_lacteos", "880040",
        "Presentación de 1.5 L de la bebida de durazno con aloe vera.",
        12, "1.5 L", 1100),
    _refresco("831390", "Ramune Fresa", "agua_gas", "831390",
        "Soda japonesa Ramune sabor fresa, con su clásica botella de canica.",
        30, "200 ml", 950),
    _refresco("831410", "Ramune Original", "agua_gas", "831410",
        "Soda japonesa Ramune sabor original, con su clásica botella de canica.",
        30, "200 ml", 950),
    _refresco("880600", "Tomomasu Soda Sabor Sandía", "agua_gas", "880600",
        "Soda artesanal japonesa sabor sandía.",
        24, "300 ml", 1225),
    _refresco("880604", "Tomomasu Soda Sabor Durazno Blanco", "agua_gas", "880604",
        "Soda artesanal japonesa sabor durazno blanco.",
        24, "300 ml", 1225),
    _refresco("880602", "Tomomasu Soda Sabor Mango", "agua_gas", "880602",
        "Soda artesanal japonesa sabor mango.",
        24, "300 ml", 1225),
]

for sort_order, refresco_product in enumerate(REFRESCOS_PRODUCTS, start=1):
    refresco_product.update(
        sort_order=sort_order,
        is_available=not refresco_product["status"].startswith("Agotado"),
    )
    apply_intl_names(refresco_product)

# The featured story cards mirror catalog pricing so one product never shows two prices.
_CATALOG_BY_ID = {p["id"]: p for p in CATALOG_PRODUCTS}
for featured in PRODUCTS:
    source = _CATALOG_BY_ID.get(featured["id"])
    if source:
        for field in ("price", "price_label", "unit_price_label", "pack_label", "pack_short",
                      "units_per_case", "unit_size", "unit_noun", "inner_packs", "promo"):
            featured[field] = source[field]
        featured["weight"] = source["pack_label"]
    apply_intl_names(featured)


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
        refrescos_products=REFRESCOS_PRODUCTS,
        refrescos_categories=REFRESCOS_CATEGORIES,
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


@app.get("/api/refrescos")
def refrescos():
    return jsonify(products=REFRESCOS_PRODUCTS)


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
    catalog_by_id = {product["id"]: product for product in [*current_catalog(), *REFRESCOS_PRODUCTS]}
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
