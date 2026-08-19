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
    {"id": "soups", "label": "Sopas y fideos"},
    {"id": "bowls", "label": "Bowls y vasos"},
    {"id": "tteokbokki", "label": "Tteokbokki"},
    {"id": "sauces", "label": "Salsas"},
    {"id": "chips", "label": "Papas y botanas"},
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


def _catalog_item(
    sku, name_es, name_en, name_zh, category, category_label, brand,
    description_es, description_en, description_zh, unit_size, source_url,
):
    """Create one local catalog row with copy for every supported language."""
    return {
        "sku": sku,
        "name": name_es,
        "name_es": name_es,
        "name_en": name_en,
        "name_zh": name_zh,
        "category": category,
        "category_label": category_label,
        "brand": brand,
        "description": description_es,
        "description_es": description_es,
        "description_en": description_en,
        "description_zh": description_zh,
        "weight": unit_size,
        "image": f"/assets/products/{sku}.webp?v=1",
        "source_url": source_url,
        "status": "Disponible",
    }


# Products from CATALAGO ACTUALIZADO MX26 that were not present in the first
# Buldak-only build. The storefront groups them by department instead of by PDF.
CATALOG_PRODUCTS.extend([
    _catalog_item(
        "811430", "Buldak Original · vaso", "Buldak Ramen Original Cup",
        "原味火鸡面（杯装）", "bowls", "Vaso", "Buldak",
        "El sabor Original en vaso individual: salsa espesa, sésamo, alga y picor directo.",
        "Original Buldak in a single cup, with thick sauce, sesame, seaweed and direct heat.",
        "经典原味杯装火鸡面，浓郁辣酱搭配芝麻与海苔，辣味直接。", "70 g",
        "https://buldak.com/us/product/buldak-ramen-original-cup/",
    ),
    _catalog_item(
        "811300", "Salsa Buldak Carbonara", "Buldak Hot Sauce Carbonara",
        "奶油味火鸡辣酱", "sauces", "Salsa", "Buldak",
        "Salsa cremosa y picante estilo Carbonara para pasta, pollo, papas o botanas.",
        "Creamy, spicy Carbonara-style sauce for pasta, chicken, fries or snacks.",
        "奶油味火鸡辣酱，适合意面、鸡肉、薯条和零食蘸食。", "200 g",
        "https://buldak.com/us/product/buldak-hot-sauce-carbonara-200g/",
    ),
    _catalog_item(
        "811280", "Salsa Buldak Original", "Buldak Hot Sauce Original",
        "原味火鸡辣酱", "sauces", "Salsa", "Buldak",
        "La salsa clásica Buldak en botella: picante, sabrosa y lista para cocinar o acompañar.",
        "Classic Buldak sauce in a bottle: hot, savory and ready for cooking or dipping.",
        "瓶装经典原味火鸡辣酱，香辣浓郁，可用于烹饪或蘸食。", "200 g",
        "https://buldak.com/us/product/buldak-hot-sauce-original-200g/",
    ),
    _catalog_item(
        "811290", "Sobres de salsa Buldak Original", "Buldak Hot Sauce Original Sticks",
        "原味火鸡辣酱便携条", "sauces", "Sobres", "Buldak",
        "Porciones individuales de salsa Original para llevar y dosificar con facilidad.",
        "Single-serve Original sauce sticks that are easy to carry and portion.",
        "原味火鸡辣酱便携条装，方便携带并精准控制用量。", "6 g",
        "https://buldak.com/us/product/buldak-hot-sauce-original-6g/",
    ),
    _catalog_item(
        "811311", "MEP ajo y almeja", "MEP Garlic & Clam Ramen",
        "MEP 蒜香蛤蜊拉面", "soups", "Sopa", "MEP",
        "Caldo marino limpio con almeja, alga y un golpe aromático de ajo.",
        "A clean seafood broth with clam, seaweed and an aromatic garlic kick.",
        "清爽海鲜汤底，融合蛤蜊、海苔与浓郁蒜香。", "120 g",
        "https://samyangamerica.com/mep/Garlic-clam",
    ),
    _catalog_item(
        "811312", "MEP res y pimienta negra", "MEP Black Pepper & Beef Ramen",
        "MEP 黑胡椒牛肉拉面", "soups", "Sopa", "MEP",
        "Caldo de res con mucho umami, pimienta negra fragante y picor en capas.",
        "Umami-rich beef broth with fragrant black pepper and layered heat.",
        "浓郁牛肉汤底，黑胡椒香气突出，辣味层次丰富。", "120 g",
        "https://samyangamerica.com/mep/Black-Pepper-Beef",
    ),
    _catalog_item(
        "811310", "MEP pollo, chile rojo y cilantro", "MEP Red Pepper, Chicken & Cilantro Ramen",
        "MEP 红椒香菜鸡肉拉面", "soups", "Sopa", "MEP",
        "Caldo ligero de pollo con chile rojo, cilantro y un final brillante de lima.",
        "Light chicken broth with red pepper, cilantro and a bright lime finish.",
        "清爽鸡汤搭配红椒、香菜与青柠尾韵。", "120 g",
        "https://samyangamerica.com/mep/red-pepper",
    ),
    _catalog_item(
        "811810", "Tangle tomate intenso", "Tangle Chunky Tomato Pasta",
        "Tangle 浓郁番茄意面", "soups", "Pasta", "Tangle",
        "Pasta instantánea con salsa de tomate espesa, ajo, cebolla y trozos de tomate.",
        "Instant pasta with chunky tomato sauce, garlic, onion and tomato pieces.",
        "即食意面搭配浓郁番茄酱、大蒜、洋葱与番茄颗粒。", "105 g",
        "https://longdan.co.uk/products/samyang-tangle-chunky-tomato-pasta-105g",
    ),
    _catalog_item(
        "811815", "Tangle bulgogi Alfredo", "Tangle Bulgogi Alfredo Big Bowl",
        "Tangle 韩式烤肉白酱意面（大碗）", "bowls", "Bowl", "Tangle",
        "Fideos anchos con salsa Alfredo cremosa y notas dulces y saladas de bulgogi.",
        "Wide noodles with creamy Alfredo sauce and sweet-savory bulgogi notes.",
        "宽面搭配奶油白酱与韩式烤肉的甜咸风味。", "105 g",
        "https://en.tangle-pasta.com/products/",
    ),
    _catalog_item(
        "811816", "Tangle crema de hongos", "Tangle Creamy Mushroom Big Bowl",
        "Tangle 奶油蘑菇意面（大碗）", "bowls", "Bowl", "Tangle",
        "Pasta cremosa con hongos, pimienta y una textura elástica de fideo ancho.",
        "Creamy mushroom pasta with pepper and bouncy wide noodles.",
        "奶油蘑菇酱搭配胡椒与弹韧宽面。", "105 g",
        "https://en.tangle-pasta.com/products/",
    ),
    _catalog_item(
        "811814", "Tangle ajo y aceite", "Tangle Garlic Oil Big Bowl",
        "Tangle 蒜香油意面（大碗）", "bowls", "Bowl", "Tangle",
        "Pasta de ajo y aceite con perejil, chile suave y fideo ancho de alta proteína.",
        "Garlic-oil pasta with parsley, gentle chili and high-protein wide noodles.",
        "蒜香油意面搭配欧芹、柔和辣椒与高蛋白宽面。", "100 g",
        "https://en.tangle-pasta.com/products/",
    ),
    _catalog_item(
        "634210", "Master Kong costilla y cebollín", "Master Kong Scallion Braised Ribs Noodle",
        "康师傅葱香排骨面", "soups", "Sopa", "Master Kong",
        "Sopa suave de costilla de cerdo con cebollín y chalota aromática.",
        "Mild pork-rib soup with scallion and aromatic shallot.",
        "温和排骨汤底，融合葱香与红葱头香气。", "104 g",
        "https://www.lunarmart.co.za/products/scallion-braised-rib-noodle",
    ),
    _catalog_item(
        "634220", "Master Kong res estofada", "Master Kong Braised Beef Noodle",
        "康师傅红烧牛肉面", "soups", "Sopa", "Master Kong",
        "El clásico caldo rojo de res estofada, profundo, especiado y reconfortante.",
        "The classic braised-beef red broth: deep, spiced and comforting.",
        "经典红烧牛肉汤底，浓郁、香料丰富且温暖满足。", "106 g",
        "https://tonymarket.shop/products/ksf-braised-beef-flavour-noodles-104g",
    ),
    _catalog_item(
        "634240", "Master Kong camarón y pastel de pescado", "Master Kong Shrimp & Fish Cake Noodle",
        "康师傅鲜虾鱼板面", "soups", "Sopa", "Master Kong",
        "Caldo marino ligero con camarón, alga y rebanadas de pastel de pescado.",
        "Light seafood broth with shrimp, seaweed and fish-cake slices.",
        "清爽海鲜汤底，搭配鲜虾、海带与鱼板。", "98 g",
        "https://www.nicedayshop.eu/product/%E5%BA%B7%E5%B8%88%E5%82%85%E9%B2%9C%E8%99%BE%E9%B1%BC%E6%9D%BF%E9%9D%A2-98g/",
    ),
    _catalog_item(
        "634250", "Master Kong res con mostaza encurtida", "Master Kong Pickled Mustard Beef Noodle",
        "康师傅老坛酸菜牛肉面", "soups", "Sopa", "Master Kong",
        "Caldo de res ácido y sabroso con mostaza encurtida al estilo tradicional.",
        "Tangy, savory beef broth with traditionally pickled mustard greens.",
        "酸爽牛肉汤底，搭配传统老坛酸菜。", "117 g",
        "https://www.lunarmart.co.za/products/beef-sour-pickle-noodles",
    ),
    _catalog_item(
        "634260", "Master Kong pollo y hongo shiitake", "Master Kong Mushroom Chicken Noodle",
        "康师傅香菇炖鸡面", "soups", "Sopa", "Master Kong",
        "Caldo suave de pollo guisado con el umami terroso del hongo shiitake.",
        "Gentle stewed-chicken broth with earthy shiitake umami.",
        "温润炖鸡汤底，融合香菇的醇厚鲜味。", "100 g",
        "https://www.ramencrate.co.nz/products/master-kang-mushroom-chicken-ramen-box",
    ),
    _catalog_item(
        "634270", "Master Kong res picante", "Master Kong Spicy Beef Noodle",
        "康师傅香辣牛肉面", "soups", "Sopa", "Master Kong",
        "Caldo rojo de res con chile, cilantro y un picor cálido y persistente.",
        "Red beef broth with chili, cilantro and warm, lingering heat.",
        "红汤牛肉面搭配辣椒与香菜，辣味温暖持久。", "104 g",
        "https://www.norexmarket.no/products/%E5%BA%B7%E5%B8%88%E5%82%85-%E9%A6%99%E8%BE%A3%E7%89%9B%E8%82%89%E9%9D%A2-inst-noodles-spicy-beef-104g",
    ),
    _catalog_item(
        "634280", "Master Kong res con pimienta verde", "Master Kong Green Peppercorn Beef Noodle",
        "康师傅藤椒牛肉面", "soups", "Sopa", "Master Kong",
        "Caldo de res con pimienta verde de Sichuan: cítrico, aromático y ligeramente adormecedor.",
        "Beef broth with green Sichuan peppercorn: citrusy, aromatic and gently numbing.",
        "牛肉汤搭配藤椒，清香柑橘感并带来轻柔麻感。", "102 g",
        "https://barakibodegon.net/products/maestro-kong-ramen-fideos-con-carne",
    ),
    _catalog_item(
        "634252", "Master Kong res con pimienta verde · bowl", "Master Kong Green Peppercorn Beef Bowl",
        "康师傅藤椒牛肉面（碗装）", "bowls", "Bowl", "Master Kong",
        "La sopa de res y pimienta verde de Sichuan en un bowl práctico de 108 g.",
        "Green Sichuan peppercorn beef soup in a convenient 108 g bowl.",
        "藤椒牛肉面碗装，108 克方便冲泡。", "108 g",
        "https://www.suning.com/item/0071470014/11027098006.html",
    ),
    _catalog_item(
        "802150", "Lay's pepino", "Lay's Cucumber Flavor Potato Chips",
        "乐事黄瓜味薯片", "chips", "Papas", "Lay's",
        "Papas delgadas con sabor fresco de pepino, sal ligera y final limpio.",
        "Thin chips with fresh cucumber flavor, light salt and a clean finish.",
        "薄脆薯片带有清新黄瓜风味、轻盐感与清爽尾韵。", "90 g",
        "https://mc.alpremium.ca/products/alp-m000692474392794",
    ),
    _catalog_item(
        "802440", "Lay's Max calamar a la parrilla", "Lay's Max Grilled Squid Flavor",
        "乐事铁板鱿鱼味大波浪薯片", "chips", "Papas", "Lay's",
        "Papas onduladas con sabor ahumado, salado y umami de calamar a la parrilla.",
        "Wavy chips with smoky, savory grilled-squid umami.",
        "大波浪薯片呈现铁板鱿鱼的烟熏咸鲜风味。", "70 g",
        "https://lilisglass.com/products/lay-s-grilled-squid-flavor",
    ),
    _catalog_item(
        "802120", "Lay's hot pot picante", "Lay's Numb & Spicy Hot Pot Flavor",
        "乐事飘香麻辣锅味薯片", "chips", "Papas", "Lay's",
        "Papas con chile, especias de hot pot y un toque ligeramente adormecedor.",
        "Chips with chili, hot-pot spices and a gently numbing finish.",
        "薯片融合辣椒与麻辣火锅香料，并带有轻微麻感。", "70 g",
        "https://candyfunhouse.ca/products/lays-numb-spicy-hot-pot-chips-china-80g",
    ),
    _catalog_item(
        "802110", "Lay's estofado italiano", "Lay's Italian Red Meat Flavor",
        "乐事意大利香浓红烩味薯片", "chips", "Papas", "Lay's",
        "Papas con tomate, hierbas y el perfil sabroso de un estofado de carne.",
        "Chips with tomato, herbs and the savory profile of a red meat stew.",
        "薯片融合番茄、香草与浓郁红烩肉风味。", "70 g",
        "https://lilisglass.com/products/lay-s-italian-red-meat-favor-70g",
    ),
    _catalog_item(
        "802410", "Lay's Max picante", "Lay's Max Pure Spicy Flavor",
        "乐事辛辣味大波浪薯片", "chips", "Papas", "Lay's",
        "Corte ondulado grueso con chile directo y textura extra crujiente.",
        "Thick wavy-cut chips with direct chili heat and extra crunch.",
        "厚切大波浪薯片，辣椒风味直接，口感格外酥脆。", "70 g",
        "https://www.joybuy.co.uk/dp/Lays-Big-Wave-Potato-Chips-Spicy/10005951",
    ),
    _catalog_item(
        "802420", "Lay's Max alita de pollo asada", "Lay's Max Roasted Chicken Wing Flavor",
        "乐事香脆烤鸡翅味大波浪薯片", "chips", "Papas", "Lay's",
        "Papas onduladas con notas de pollo asado, ajo, dulzor suave y humo.",
        "Wavy chips with roasted chicken, garlic, gentle sweetness and smoke.",
        "大波浪薯片融合烤鸡翅、蒜香、微甜与烟熏风味。", "70 g",
        "https://theexoticclub.com/products/lays-roasted-chicken-wing-flavor-asia",
    ),
    _catalog_item(
        "802160", "Lay's cangrejo dorado", "Lay's Golden Fried Crab Flavor",
        "乐事金黄炒蟹味薯片", "chips", "Papas", "Lay's",
        "Papas crujientes con cangrejo salado, un punto dulce y acabado marino.",
        "Crisp chips with savory crab, gentle sweetness and a seafood finish.",
        "酥脆薯片呈现咸鲜蟹味、微甜感与海鲜尾韵。", "70 g",
        "https://popshoplife.com/products/lays-fried-crab-flavor-china",
    ),
    _catalog_item(
        "854170", "Want Want rollos sabor verduras", "Want Want Lonely God Vegetable Potato Rolls",
        "旺旺浪味仙田园蔬菜味", "chips", "Botana", "Want Want",
        "Rollos ligeros de papa con cebollín, ajo y un condimento suave de verduras.",
        "Light potato rolls with scallion, garlic and mild vegetable seasoning.",
        "轻盈花式薯卷，融合葱香、蒜香与柔和田园蔬菜味。", "70 g",
        "https://www.yami.com/zh/p/fruit-melty-sticks-strawberry-dragon-fruit-apple-flavor-18g/3150016651",
    ),
    _catalog_item(
        "854180", "Want Want rollos sabor alga", "Want Want Lonely God Seaweed Potato Rolls",
        "旺旺浪味仙海苔味", "chips", "Botana", "Want Want",
        "Rollos crujientes de papa con alga tostada y un final salado lleno de umami.",
        "Crisp potato rolls with roasted seaweed and a savory umami finish.",
        "酥脆花式薯卷搭配烤海苔，咸鲜味十足。", "70 g",
        "https://www.cvmart.co.uk/product-10206.html",
    ),
])


# Wholesale packing taken from the three supplied price lists: how many retail
# units travel inside one case, the size of each unit, and the price of that case.
# (units, unit_size, case_price, unit_noun)
CATALOG_PACKS = {
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
    "811650": (12, "169.4 g", 1020, "bowls"),
    "811710": (16, "179 g", 928, "bowls"),
    "811720": (16, "185 g", 928, "bowls"),
    "811910": (12, "120 g", 900, "bolsas"),
    "811920": (12, "120 g", 900, "bolsas"),
    "811430": (6, "70 g", 186, "vasos"),
    "811300": (24, "200 g", 2640, "botellas"),
    "811280": (24, "200 g", 2688, "botellas"),
    "811290": (200, "6 g", 1000, "sobres", 50),
    "811311": (32, "120 g", 896, "bolsas"),
    "811312": (32, "120 g", 896, "bolsas"),
    "811310": (32, "120 g", 896, "bolsas"),
    "811810": (32, "105 g", 1024, "bolsas"),
    "811815": (6, "105 g", 354, "bowls"),
    "811816": (6, "105 g", 354, "bowls"),
    "811814": (6, "100 g", 354, "bowls"),
    "634210": (30, "104 g", 507, "bolsas", 5),
    "634220": (30, "106 g", 507, "bolsas", 5),
    "634240": (30, "98 g", 507, "bolsas", 6),
    "634250": (30, "117 g", 507, "bolsas", 5),
    "634260": (30, "100 g", 507, "bolsas", 5),
    "634270": (30, "104 g", 507, "bolsas", 5),
    "634280": (30, "102 g", 507, "bolsas", 5),
    "634252": (12, "108 g", 384, "bowls"),
    "802150": (24, "90 g", 912, "bolsas"),
    "802440": (22, "70 g", 770, "bolsas"),
    "802120": (22, "70 g", 770, "bolsas"),
    "802110": (22, "70 g", 770, "bolsas"),
    "802410": (22, "70 g", 770, "bolsas"),
    "802420": (22, "70 g", 770, "bolsas"),
    "802160": (22, "70 g", 770, "bolsas"),
    "854170": (12, "70 g", 456, "bolsas"),
    "854180": (12, "70 g", 456, "bolsas"),
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


# Export names retained from the earlier catalog. The second value is legacy
# Japanese copy and is intentionally not exposed by the three-language UI.
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

ZH_NAMES = {
    "811140": "奶油味火鸡面", "811130": "奶油干酪味火鸡面", "811200": "芝士味火鸡面",
    "811150": "芝士联盟火鸡面", "811270": "玫瑰奶油味火鸡面", "811320": "焦糖甜辣味火鸡面",
    "811000": "塔可味火鸡面", "811340": "日式炒面味火鸡面", "811220": "哈瓦那辣椒青柠味火鸡面",
    "811120": "原味火鸡面", "811210": "双倍辣火鸡面", "811616": "焦糖甜辣味火鸡面（大碗）",
    "811618": "芝士联盟火鸡面（大碗）", "811622": "奶油味火鸡面（大碗）",
    "811624": "原味火鸡面（大碗）", "811640": "玫瑰奶油味火鸡面（大碗）",
    "811650": "玫瑰奶油味宽粉", "811612": "原味火鸡面（大碗）", "811710": "奶油味火鸡炒年糕",
    "811720": "原味火鸡炒年糕", "811910": "哈瓦那辣椒青柠味火鸡薯片", "811920": "原味火鸡薯片",
    "833130": "椰树椰汁", "833210": "王老吉凉茶", "831190": "元气森林白桃味气泡水",
    "194280": "维他蜜桃茶", "880350": "宾格瑞哈密瓜牛奶", "831214": "元气森林柠檬可乐味气泡水",
    "834510": "水泉湾乳酸菌饮品", "832110": "康师傅茉莉花茶", "832160": "康师傅冰糖雪梨",
    "832140": "康师傅蜂蜜柚子茶", "831831": "山楂树下山楂汁", "837410": "365绿茶 柠檬香茅味",
    "837412": "365绿茶 蜂蜜味", "831160": "元气森林荔枝味气泡水", "831220": "元气森林白桃味气泡水（罐装）",
    "831170": "元气森林葡萄味气泡水", "831140": "元气森林橙子味气泡水", "831240": "元气森林荔枝味气泡水（罐装）",
    "833320": "泰山仙草蜜 原味", "833330": "泰山仙草蜜 荔枝味", "833340": "泰山仙草蜜 椰子味",
    "837520": "J WAY 鲜果茶波霸套装", "837510": "J WAY 奶茶波霸套装", "838210": "东鹏补水啦 柠檬味",
    "838212": "东鹏补水啦 西柚味", "838214": "东鹏补水啦 荔枝味", "838312": "东鹏补水啦 柠檬味 555ml",
    "838314": "东鹏补水啦 荔枝味 555ml", "838310": "东鹏补水啦 西柚味 555ml", "880910": "海太葡萄汁",
    "880010": "芦荟芒果饮料", "880020": "芦荟芒果饮料 1.5L", "880030": "芦荟草莓饮料",
    "880040": "芦荟白桃饮料 1.5L", "831390": "弹珠汽水 草莓味", "831410": "弹珠汽水 原味",
    "880600": "友桝西瓜汽水", "880604": "友桝白桃汽水", "880602": "友桝芒果汽水",
}


def apply_intl_names(product):
    """Attach language-ready display copy without changing the database row."""
    name_en, _legacy_name = INTL_NAMES.get(product["sku"], (product["name"], ""))
    product["name_es"] = product.get("name_es") or product["name"]
    product["name_en"] = product.get("name_en") or name_en
    product["name_zh"] = product.get("name_zh") or ZH_NAMES.get(product["sku"], product["name"])
    product["description_es"] = product.get("description_es") or product.get("description") or f"{product['name_es']} de {product.get('brand', 'Buldak')}, disponible por caja cerrada."
    product["description_en"] = product.get("description_en") or f"{product['name_en']}, available by wholesale full case."
    product["description_zh"] = product.get("description_zh") or f"{product['name_zh']}，按批发整箱出售。"
    return product


for sort_order, catalog_product in enumerate(CATALOG_PRODUCTS, start=1):
    # Older rows used product-format categories; the complete store uses the
    # three departments requested by the shop owner.
    if catalog_product["category"] == "bags":
        catalog_product.update(category="soups", category_label="Sopa y fideos")
    elif catalog_product["category"] == "snacks":
        catalog_product.update(category="chips", category_label="Papas y botanas")
    catalog_product.setdefault("brand", "Buldak")
    catalog_product.update(
        id=catalog_product["sku"],
        sort_order=sort_order,
        is_available=not catalog_product["status"].startswith("Agotado"),
    )
    apply_pack(catalog_product, *CATALOG_PACKS[catalog_product["sku"]])
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
    brand_by_prefix = {
        "833130": "Coconut Palm", "833210": "Wong Lo Kat", "194280": "Vita",
        "880350": "Binggrae", "834510": "Shui Lian Wan", "831831": "Shan Zha Shu Xia",
        "837410": "MASAN", "837412": "MASAN", "837520": "J WAY", "837510": "J WAY",
        "880910": "Haitai", "831390": "Ramune", "831410": "Ramune",
    }
    if refresco_product["sku"].startswith("831") and refresco_product["sku"] not in brand_by_prefix:
        brand = "Chi Forest"
    elif refresco_product["sku"].startswith("832"):
        brand = "Master Kong"
    elif refresco_product["sku"].startswith("8333"):
        brand = "Taisun"
    elif refresco_product["sku"].startswith("838"):
        brand = "Dongpeng"
    elif refresco_product["sku"].startswith("8800"):
        brand = "Yogo Vera"
    elif refresco_product["sku"].startswith("8806"):
        brand = "Tomomasu"
    else:
        brand = brand_by_prefix.get(refresco_product["sku"], "Importación asiática")
    refresco_product.update(
        sort_order=sort_order,
        is_available=not refresco_product["status"].startswith("Agotado"),
        brand=brand,
    )
    apply_intl_names(refresco_product)


BRANDS = [
    {"name": "Buldak", "kind": "noodles"},
    {"name": "Samyang", "kind": "noodles"},
    {"name": "MEP", "kind": "noodles"},
    {"name": "Tangle", "kind": "noodles"},
    {"name": "Master Kong", "kind": "noodles"},
    {"name": "Lay's", "kind": "snacks"},
    {"name": "Want Want", "kind": "snacks"},
    {"name": "Chi Forest", "kind": "drinks"},
    {"name": "Vita", "kind": "drinks"},
    {"name": "Binggrae", "kind": "drinks"},
    {"name": "Coconut Palm", "kind": "drinks"},
    {"name": "Wong Lo Kat", "kind": "drinks"},
    {"name": "Shui Lian Wan", "kind": "drinks"},
    {"name": "MASAN", "kind": "drinks"},
    {"name": "Taisun", "kind": "drinks"},
    {"name": "J WAY", "kind": "drinks"},
    {"name": "Dongpeng", "kind": "drinks"},
    {"name": "Haitai", "kind": "drinks"},
    {"name": "Yogo Vera", "kind": "drinks"},
    {"name": "Ramune", "kind": "drinks"},
    {"name": "Tomomasu", "kind": "drinks"},
    {"name": "Shan Zha Shu Xia", "kind": "drinks"},
]

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
    """Merge editable Supabase rows with the complete catalog shipped in code.

    This lets the production database continue controlling availability and
    product imagery while newly catalogued SKUs appear immediately, even before
    a database migration is applied.
    """
    stored = repository.list_products(CATALOG_PRODUCTS)
    stored_by_sku = {str(product["sku"]): product for product in stored}
    catalog = []
    for local in CATALOG_PRODUCTS:
        product = {**local, **stored_by_sku.get(str(local["sku"]), {})}
        # Department, brand and translated copy are versioned with the site.
        for field in (
            "category", "category_label", "brand", "name_es", "name_en", "name_zh",
            "description", "description_es", "description_en", "description_zh",
        ):
            if field in local:
                product[field] = local[field]
        pack = CATALOG_PACKS.get(product["sku"])
        if pack:
            apply_pack(product, *pack)
            product["case"] = product["pack_label"]
        apply_intl_names(product)
        catalog.append(product)
    return catalog


def carousel_catalog(catalog_products: list[dict]) -> list[dict]:
    """Keep three Buldak packs first, soups next, bowls mid-list and chips last."""
    lead_ids = ("811120", "811140", "811150")
    product_by_id = {str(product["id"]): product for product in catalog_products}
    lead = [product_by_id[product_id] for product_id in lead_ids if product_id in product_by_id]
    lead_set = set(lead_ids)
    remainder = [product for product in catalog_products if str(product["id"]) not in lead_set]
    category_order = {"soups": 0, "bowls": 1, "tteokbokki": 2, "sauces": 3, "chips": 4}
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
        brands=BRANDS,
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
