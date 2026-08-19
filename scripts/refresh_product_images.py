"""Refresh new catalog images from the best verified product sources available."""

from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path
from urllib.parse import urlsplit

import requests
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "frontend" / "assets" / "products"
PREVIEW_DIR = ROOT / "tmp" / "product-image-preview"
MAX_SIDE = 1400
MASK_SIDE = 520
BACKGROUND_THRESHOLD = 24

# Every URL below was matched against the exact package name/SKU before use.
SOURCES = {
    "061010": "https://img06.weeecdn.com/item/image/642/361/5FAAC9003286A98A.png",
    "061020": "https://cdn.yamibuy.net/item/59e23652804e34d23d3692b3c03e211f_640x640.webp",
    "061030": "https://img08.weeecdn.net/item/image/467/899/53E0C9ECE12AD447.png%21c750x0_q80_t1.auto",
    "061050": "https://img06.weeecdn.com/product/image/845/490/156B29CC43ABF15F.png%21c750x0.jpeg",
    "061060": "https://img06.weeecdn.com/item/image/152/243/45C0DBE386254BF4.webp%21c750x0.jpeg",
    "061080": "https://p16-oec-general-useast5.ttcdn-us.com/tos-useast5-i-omjb5zjo8w-tx/dd86231a49ab4be885f8004e58b1438e~tplv-fhlh96nyum-crop-webp%3A1182%3A1182.webp?dr=12190&from=2378011839&idc=useast5&ps=933b5bde&shcp=e1be8f53&shp=8dbd94bf&t=555f072d",
    "164397": "https://img06.weeecdn.com/item/image/043/518/3742ACE1BA01254E.png",
    "164398": "https://img06.weeecdn.com/item/image/544/402/34E8A5B0BD25309A.png",
    "634210": "https://www.lunarmart.co.za/cdn/shop/files/Master_Kang_Scallion_Braised_Rib_Noodle_104g_1.png?crop=center&height=1200&v=1740666830&width=1200",
    "634220": "https://wenzhousupermercados.com/17509-large_default/-24-100g.jpg",
    "634240": "https://imgservice.suning.cn/uimg1/b2c/image/jkzqCcSPsa9_SYXeWVZSNw.jpg_800w_800h_4e_80Q_is",
    "634250": "https://www.lunarmart.co.za/cdn/shop/files/MasterKangPickledVegetableBeefNoodle117g_1.png?crop=center&height=1200&v=1740666904&width=1200",
    "634252": "https://imgservice.suning.cn/uimg1/b2c/image/VB3v2f9xHLSAtwvL_WtdTw.png",
    "634260": "https://www.ramencrate.co.nz/cdn/shop/files/MasterKangMushroomChickenInstantNoodles.png?v=1742727989",
    "634270": "https://huongvietstore.co.uk/cdn/shop/files/MeisterKongnudelnsuppeRindscharf.webp?crop=center&height=1200&v=1762779315&width=1200",
    "634280": "https://barakibodegon.net/cdn/shop/files/ramen5.jpg?v=1718666386&width=1946",
    "802110": "https://lilisglass.com/cdn/shop/products/image_a854ff46-73f8-4990-90ed-4e2c4653c632.png?v=1634160370&width=1024",
    "802120": "https://candyfunhouse.ca/cdn/shop/files/lays-numb-spicy-hot-pot-chips-china-80g-Candy-Funhouse.png?v=1763477983",
    "802150": "https://cdn.yamibuy.net/item/84cbd4dab38bd83eb93e2e92c6ab7ab9_757x757.webp",
    "802160": "https://popshoplife.com/cdn/shop/files/Lay_sFriedCrabFlavor_70g_China_406c5d97-0be2-41fe-b78d-8489fa6681b4_1024x1024.jpg?v=1684897045",
    "802410": "https://images4.joy-sourcing.com/product/s1248x1248_jfsintlpro-000-product/t1/4294967296/3407872/62073657722/1004936/69ccdd99E9b13344c/42b10752b5083d5e.png.webp",
    "802420": "https://theexoticclub.com/cdn/shop/files/LaysRoastedChickenWingchips70g-China_1200x1200.jpg?v=1710985744",
    "802440": "https://lilisglass.com/cdn/shop/products/image_22792174-9c28-4530-87ae-6804675e1394_2048x.jpg?v=1601085915",
    "806160": "https://hiyou.co/cdn/shop/products/0024106_1028x.jpg?v=1646329086",
    "806170": "https://hiyou.co/cdn/shop/products/0024107_1028x.jpg?v=1646328960",
    "807331": "https://thaipiac.cdn.shoprenter.hu/custom/thaipiac/image/cache/w900h900wt1q100/product/62293.webp?lastmod=0.1683619129",
    "807341": "https://thaipiac.cdn.shoprenter.hu/custom/thaipiac/image/cache/w900h900wt1q100/product/62292.webp?lastmod=0.1683619129",
    "807810": "https://img06.weeecdn.com/item/image/583/453/19D4C57F5A301F27.jpeg%21c750x0.jpeg",
    "811280": "https://cdn.buldak.com/images_dev/1758262936762-1_US_Sauce_original.png",
    "811290": "https://cdn.buldak.roundsquare.io/en/uploads/2025/03/20250312_043142.png",
    "811300": "https://cdn.buldak.com/images_dev/1758263103390-2_US_Sauce_Carbonara.png",
    "811310": "https://samyangamerica.com/images/products/mep-Redc-Pepper.png",
    "811311": "https://samyangamerica.com/images/products/mep-Garlic-Clam.png",
    "811312": "https://samyangamerica.com/images/products/mep-Black-Pepper-Beef.png",
    "811430": "https://cdn.buldak.roundsquare.io/en/uploads/2025/03/20250312_032902.png",
    "811611": "https://cdn.buldak.roundsquare.io/en/uploads/2025/03/20250312_033422.png",
    "811810": "https://longdan.co.uk/cdn/shop/files/4512861_1600x.png?v=1761560046",
    "851110": "https://cdn.yamibuy.net/item/a359aca877fb8d4b4a0bb339964de053_750x750.webp",
    "851120": "https://img10.360buyimg.com/n1/s720x720_jfs/t1/374131/11/18819/379253/69464d70F85f0f91a/fc888f6877ca77be.jpg",
    "851122": "https://globalbiteco.com/cdn/shop/files/output-onlinepngtools_27_bf972807-0ae5-4743-a69a-fff2a573475f.png?v=1744673620",
    "851124": "https://globalbiteco.com/cdn/shop/files/output-onlinepngtools_28_fc514f31-385b-4df7-afd5-a2728d6b3da0_grande.png?v=1744673751",
    "851160": "https://robohunters.com/cdn/shop/files/8aea84325b6a0862847364666b9289f6_757x757_3dfdb3d2-0438-4fe4-a177-c11d76b44d24.jpg?v=1746049129",
    "851180": "https://img08.weeecdn.net/item/image/648/209/1AB8A3E60F0DF191.png%21c864x0_q80.auto",
    "851192": "https://img08.weeecdn.net/item/image/450/289/85F7E53AC3ED269.png.jpeg%21c864x0_q80.auto",
    "851210": "https://img06.weeecdn.com/item/image/623/690/2045670B5F57CC06.jpeg",
    "851220": "https://asianpantry.com.au/cdn/shop/files/498f141eec7fb918ca602e16537b7708.webp?v=1748473990&width=1920",
    "851230": "https://imgservice.suning.cn/uimg1/b2c/image/qOieREfVgXoDFroEvRqsGQ.jpg_800w_800h_4e",
    "851430": "https://img06.weeecdn.com/product/image/084/622/585F4481CB61FB64.png",
    "851510": "https://gw.alicdn.com/imgextra/i1/752373698/O1CN01AHQ7og1dBjT8dj2vD_%21%21752373698.jpg",
    "851800": "https://beautycornerca.com/cdn/shop/files/alioss_2_2022061514421925454.jpg?v=1684985741",
    "851820": "https://filebroker-cdn.lazada.com.my/kf/Sbb39e175079a413f8fd6b124fa63e77ez.jpg",
    "854170": "https://image.umall.com.au/image/goods4/A6905734301031/image/1.jpg?x-oss-process=image%2Fresize%2Cw_750%2Fsharpen%2C100%2Fquality%2CQ_100",
    "854180": "https://pongmarket.se/thumb/14309/1280x0/PMS-SK0804_1.png",
    "854190": "https://www.foodforfoodies.co.uk/cdn/shop/files/fcd68bb0-d089-4fc6-b99c-ccd83a7163db_4000000000000980_1_1200x1200.jpg?v=1768553515",
    "854200": "https://image.umall.com.au/product/A6931958068290/image/1.jpg?x-oss-process=image%2Fresize%2Cw_750%2Fsharpen%2C100%2Fquality%2CQ_100",
    "854210": "https://asianpantry.com.au/cdn/shop/files/60badfaebe258d9106705a4dd4047607.webp?v=1765430950&width=1500",
    "880700": "https://pinoygroseri.com/cdn/shop/files/PockyChocolate70g_Front_1337x.png?v=1733161498",
    "880701": "https://himall-storage-1259069382.cos.ap-nanjing.myqcloud.com/web/Storage/Shop/1346/Products/57337/1.png",
}


def download(session: requests.Session, url: str) -> Image.Image:
    split = urlsplit(url)
    headers = {"Referer": f"{split.scheme}://{split.netloc}/"}
    response = session.get(url, headers=headers, timeout=40)
    response.raise_for_status()
    if len(response.content) < 8_000:
        raise ValueError(f"download too small ({len(response.content)} bytes)")
    return Image.open(BytesIO(response.content)).convert("RGBA")


def exterior_mask(image: Image.Image) -> Image.Image | None:
    """Remove only a connected, nearly uniform backdrop from the image border."""
    rgb = image.convert("RGB")
    sample = rgb.resize((1, 1), Image.Resampling.BOX).getpixel((0, 0))
    corners = [rgb.getpixel(point) for point in ((0, 0), (rgb.width - 1, 0), (0, rgb.height - 1), (rgb.width - 1, rgb.height - 1))]
    spread = max(max(color[i] for color in corners) - min(color[i] for color in corners) for i in range(3))
    if spread > 48:
        return None

    small = rgb.copy()
    small.thumbnail((MASK_SIDE, MASK_SIDE), Image.Resampling.LANCZOS)
    marker = (1, 2, 3)
    for seed in ((0, 0), (small.width - 1, 0), (0, small.height - 1), (small.width - 1, small.height - 1)):
        ImageDraw.floodfill(small, seed, marker, thresh=BACKGROUND_THRESHOLD)
    difference = ImageChops.difference(small, Image.new("RGB", small.size, marker))
    mask = ImageChops.lighter(ImageChops.lighter(difference.getchannel("R"), difference.getchannel("G")), difference.getchannel("B"))
    mask = mask.point(lambda value: 0 if value == 0 else 255)
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    return mask.resize(image.size, Image.Resampling.LANCZOS)


def normalize(source: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(source).convert("RGBA")
    original_alpha = image.getchannel("A")
    backdrop_alpha = exterior_mask(image)
    if backdrop_alpha is not None:
        image.putalpha(ImageChops.multiply(original_alpha, backdrop_alpha))

    bbox = image.getbbox()
    if bbox:
        image = image.crop(bbox)
    image.thumbnail((MAX_SIDE, MAX_SIDE), Image.Resampling.LANCZOS)
    padding = max(34, round(max(image.size) * 0.055))
    canvas_side = min(MAX_SIDE + padding * 2, max(720, max(image.size) + padding * 2))
    canvas = Image.new("RGBA", (canvas_side, canvas_side), (255, 255, 255, 0))
    canvas.alpha_composite(image, ((canvas_side - image.width) // 2, (canvas_side - image.height) // 2))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="write to tmp instead of replacing catalog assets")
    parser.add_argument("skus", nargs="*", help="optional SKU subset")
    args = parser.parse_args()
    destination = PREVIEW_DIR if args.preview else PRODUCTS_DIR
    destination.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        }
    )

    failures = []
    selected_sources = {sku: url for sku, url in SOURCES.items() if not args.skus or sku in args.skus}
    for sku, url in selected_sources.items():
        try:
            source = download(session, url)
            output = normalize(source)
            target = destination / f"{sku}.webp"
            output.save(target, "WEBP", quality=92, method=5, alpha_quality=100)
            print(f"{sku}: {source.width}x{source.height} -> {output.width}x{output.height}")
        except Exception as exc:  # noqa: BLE001
            failures.append((sku, type(exc).__name__, str(exc)))
            print(f"{sku}: ERROR {type(exc).__name__}: {exc}")

    if failures:
        raise SystemExit(f"{len(failures)} image downloads failed: {failures}")
    print(f"Refreshed {len(selected_sources)} product images in {destination}")


if __name__ == "__main__":
    main()
