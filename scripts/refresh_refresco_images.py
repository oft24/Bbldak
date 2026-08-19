"""Refresh soft drink photography from verified high-resolution sources.

The source list deliberately uses exact product/flavour matches. Downloaded
PNG/JPEG/WebP originals are normalized to a consistent transparent 1600 px
catalog canvas and stored as efficient WebP assets used by the storefront.
"""

from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path
from urllib.parse import urlsplit

import requests
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
REFRESCOS_DIR = ROOT / "frontend" / "assets" / "refrescos"
PREVIEW_DIR = ROOT / "tmp" / "refresco-image-preview"
CANVAS_SIDE = 1600
MASK_SIDE = 560
BACKGROUND_THRESHOLD = 22
MIN_SOURCE_LONG_SIDE = 600
MIN_PRODUCT_SIDE = 420

# Exact flavour/presentation matches found during the August 2026 audit.
SOURCES = {
    "194280": "https://www.superwafer.ca/storage/products/October2022/oLbrzXnEl5SZottECZ3u.png",
    "831180": "https://www.tastysnack.asia/cdn/shop/files/ChiForest-GreenAppleSparklingWaterBottle_480ml_1024x.png?v=1751945815",
    "831220": "https://hiyou.co/cdn/shop/products/0025062_1200x1200.jpg?v=1663160014",
    "831230": "https://hiyou.co/cdn/shop/products/0025061_1200x1200.jpg?v=1663160184",
    "831240": "https://hiyou.co/cdn/shop/products/0025064_1200x1200.jpg?v=1662988544",
    "831250": "https://i5.walmartimages.com/seo/Chi-Forest-Sparkling-Water-Orange-11-15-oz-Can-Case-of-24_29342d15-4c87-41cd-b1ce-d4c23d45534a.ddf7133518de7ac6426583a85575e176.png?odnBg=FFFFFF&odnHeight=768&odnWidth=768",
    "831270": "https://digitalcontent.api.tesco.com/v2/media/ghs/5fb7c723-dd4f-4cde-8c21-d59a18d6847a/e51fb611-77dc-4066-8bae-ee3370b0a133_2013204561.jpeg?h=960&w=960",
    "831290": "https://hiyou.co/cdn/shop/products/0025065_1200x1200.jpg?v=1662988346",
    "831310": "https://trovasia.com/cdn/shop/files/acqua-elettrolitica-al-lime-500ml-920462.webp?v=1753556441",
    "831320": "https://hiyou.co/cdn/shop/files/6970399927247_506ebceb-32da-464b-b4b5-06320ad2ec10_1200x1200.jpg?v=1752059100",
    "831430": "https://cdn.shopify.com/s/files/1/0250/7483/products/hata-kosen-ramune-orange-200mL-japan-candyfunhouse_1600x.jpg?v=1654797692",
    "831490": "https://www.godtesjuk.no/users/godtesjuk_mystore_no/images/U4tOP_Hata_Kosen_Hata_Kosen_Bottle_Ramune_Yuzu_200_1.png",
    "831830": "https://img06.weeecdn.com/product/image/537/736/3F3D5634D1812D27.png",
    "832120": "https://img06.weeecdn.com/item/image/829/857/6F82FC761552F593.jpg",
    "832130": "https://img06.weeecdn.com/item/image/583/152/2D010113C02C7880.png.jpeg",
    "832150": "https://hmartus.vtexassets.com/arquivos/ids/177154/692245680516.png?v=639052352318700000",
    "832180": "https://www.alimentacionasiatica.com/cdn/shop/products/bebidadeciruelas500mlksf_1000x.png?v=1670860996",
    "833110": "https://images4.joy-sourcing.com/product/s1248x1248_jfsintlpro-000-product/t1/4294967296/2752512/6109796642351/431308/69660b41Ee585d1b4/42b10752b5083d5e.png.webp",
    "833720": "https://www.japanhomeeshop.com/cdn/shop/files/4909411084950_1200x1200.jpg?v=1776303806",
    "834520": "https://globalbiteco.com/cdn/shop/files/101B-0051-1_1200x1200_6d852bb7-899f-4a65-bb1a-5a694b872132.webp?v=1708636396",
    "834530": "https://hmartus.vtexassets.com/arquivos/ids/172630/697111760004.png?v=638860451098830000",
    "836110": "https://img06.weeecdn.com/product/image/013/041/7D12D3DD5F81318B.png",
    "837110": "https://drug-platform.cdn.bcebos.com/online/drug/d1651209882547284543.png?x-bce-process=image%2Fauto-orient%2Co_1%2Fresize%2Cw_1242%2Climit_1%2Fquality%2CQ_85%2Fformat%2Cf_auto",
    "837210": "https://img06.weeecdn.com/description/image/431/303/4ACF8CF6580A54D.png",
    "871110": "https://www.instacart.com/image-server/1200x1200/www.instacart.com/assets/domains/product-image/file/large_1d1ae5e6-b184-4a3e-9ab1-11fa823bf464.jpg",
    "880020": "https://a.fsimg.co.nz/product/retail/fan/image/master/5032308.png",
    "880030": "https://www.instacart.com/image-server/1200x1200/www.instacart.com/assets/domains/product-image/file/large_f02a7c82-2be4-468a-899c-1eb8d63f64f2.jpg",
    "880170": "https://tastysnack.id/cdn/shop/files/26_1ff691af-8129-4bd9-98d7-cd4be578a573_1200x1200.png?v=1728967575",
    "880210": "https://axiastation.ca/cdn/shop/files/4993.webp?v=1765727582",
    "880220": "https://axiastation.ca/cdn/shop/files/27371.jpg?v=1756947864",
    "880230": "https://gracemarketks.com/cdn/shop/products/Gugencoconutmilkstrawberry.jpg?v=1619289546",
    "880330": "https://hebmx.vtexassets.com/arquivos/ids/925635/1006845_image-1743051588.jpg?v=638787624842000000",
    "880340": "https://www.tteokbokki.vn/cdn/shop/files/Sua-dau-Binggrae-hop-200ml.png?v=1742451995",
    "880360": "https://www.tteokbokki.vn/cdn/shop/files/Sua-khoai-mon-Binggrae-200ml.png?v=1718952834",
    "880370": "https://mam-shop.fr/cdn/shop/files/2100000127559_compressed_efd8f2e3-f07a-44d9-a9e0-d7cb68f87154.webp?v=1772708123&width=1445",
    "880910": "https://cdn.yamibuy.net/item/6196ddcf8bbf27ee672505d865408a12_750x750.webp",
    "880601": "https://img06.weeecdn.com/description/image/641/854/433681742ACE4815.png",
    "A72103": "https://m.media-amazon.com/images/I/81WL7pzs2YL._SL1000_.jpg",
}

TRIM_WHITE_CANVAS = {"832180"}


def download(session: requests.Session, url: str) -> Image.Image:
    split = urlsplit(url)
    response = session.get(
        url,
        headers={"Referer": f"{split.scheme}://{split.netloc}/"},
        timeout=45,
    )
    response.raise_for_status()
    if len(response.content) < 12_000:
        raise ValueError(f"download too small ({len(response.content)} bytes)")
    image = Image.open(BytesIO(response.content))
    image.load()
    if max(image.size) < MIN_SOURCE_LONG_SIDE:
        raise ValueError(f"source resolution too small ({image.width}x{image.height})")
    return ImageOps.exif_transpose(image).convert("RGBA")


def exterior_alpha(image: Image.Image) -> Image.Image | None:
    """Remove a connected, near-white backdrop without erasing white labels."""
    rgb = image.convert("RGB")
    corners = [
        rgb.getpixel(point)
        for point in ((0, 0), (rgb.width - 1, 0), (0, rgb.height - 1), (rgb.width - 1, rgb.height - 1))
    ]
    if min(min(color) for color in corners) < 205:
        return None
    small = rgb.copy()
    small.thumbnail((MASK_SIDE, MASK_SIDE), Image.Resampling.LANCZOS)
    marker = (1, 2, 3)
    for seed in ((0, 0), (small.width - 1, 0), (0, small.height - 1), (small.width - 1, small.height - 1)):
        ImageDraw.floodfill(small, seed, marker, thresh=BACKGROUND_THRESHOLD)
    difference = ImageChops.difference(small, Image.new("RGB", small.size, marker))
    mask = ImageChops.lighter(
        ImageChops.lighter(difference.getchannel("R"), difference.getchannel("G")),
        difference.getchannel("B"),
    ).point(lambda value: 0 if value == 0 else 255)
    return mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7)).resize(
        image.size, Image.Resampling.LANCZOS
    )


def trim_white_canvas(image: Image.Image) -> Image.Image:
    """Tightly crop a product supplied on a large opaque-white square."""
    rgb = Image.alpha_composite(Image.new("RGBA", image.size, "white"), image).convert("RGB")
    difference = ImageChops.difference(rgb, Image.new("RGB", rgb.size, "white"))
    mask = ImageChops.lighter(
        ImageChops.lighter(difference.getchannel("R"), difference.getchannel("G")),
        difference.getchannel("B"),
    ).point(lambda value: 255 if value > 18 else 0)
    bbox = mask.getbbox()
    if not bbox:
        return image
    margin = max(12, round(max(image.size) * 0.035))
    left, top, right, bottom = bbox
    return image.crop(
        (
            max(0, left - margin),
            max(0, top - margin),
            min(image.width, right + margin),
            min(image.height, bottom + margin),
        )
    )


def normalize(source: Image.Image, sku: str) -> Image.Image:
    image = source.copy()
    if sku in TRIM_WHITE_CANVAS:
        image = trim_white_canvas(image)
    source_has_alpha = image.getchannel("A").getextrema()[0] < 255
    detected_alpha = exterior_alpha(image)
    if detected_alpha is not None:
        image.putalpha(ImageChops.multiply(image.getchannel("A"), detected_alpha))
    elif not source_has_alpha:
        raise ValueError("source background is not clean or removable")
    bbox = image.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
    if bbox:
        image = image.crop(bbox)
    if max(image.size) < MIN_PRODUCT_SIDE:
        raise ValueError(f"isolated product is too small ({image.width}x{image.height})")
    scale = min(1360 / image.width, 1360 / image.height)
    image = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("RGBA", (CANVAS_SIDE, CANVAS_SIDE), (255, 255, 255, 0))
    canvas.alpha_composite(image, ((CANVAS_SIDE - image.width) // 2, (CANVAS_SIDE - image.height) // 2))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skus", nargs="*", help="optional SKU subset")
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    destination = PREVIEW_DIR if args.preview else REFRESCOS_DIR
    destination.mkdir(parents=True, exist_ok=True)

    selected = {sku: url for sku, url in SOURCES.items() if not args.skus or sku in args.skus}
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 Chrome/139 Safari/537.36"
    failures = []
    for sku, url in selected.items():
        try:
            source = download(session, url)
            output = normalize(source, sku)
            output.save(destination / f"{sku}.webp", "WEBP", quality=92, method=4, alpha_quality=100)
            print(f"{sku}: {source.width}x{source.height} -> {output.width}x{output.height}")
        except Exception as exc:  # noqa: BLE001
            failures.append((sku, type(exc).__name__, str(exc)))
            print(f"{sku}: ERROR {type(exc).__name__}: {exc}")
    if failures:
        raise SystemExit(f"{len(failures)} downloads failed: {failures}")
    print(f"Refreshed {len(selected)} verified drink images in {destination}")


if __name__ == "__main__":
    main()
