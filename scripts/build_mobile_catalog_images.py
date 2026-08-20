"""Build lightweight catalog images for narrow, high-density phone screens."""

from __future__ import annotations

from pathlib import Path
import sys
from urllib.parse import urlsplit

from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from backend.app import CATALOG_PRODUCTS, FRONTEND_DIR, REFRESCOS_PRODUCTS


OUTPUT_DIR = FRONTEND_DIR / "assets" / "mobile-catalog"
MAX_EDGE = 640


def source_path(image_url: str) -> Path:
    clean_path = urlsplit(image_url).path.removeprefix("/assets/")
    return FRONTEND_DIR / "assets" / clean_path


def build_image(product: dict) -> tuple[int, int]:
    source = source_path(product["image"])
    target = OUTPUT_DIR / f"{product['sku']}.webp"
    before = source.stat().st_size

    with Image.open(source) as image:
        image.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        has_alpha = "A" in image.getbands()
        prepared = image.convert("RGBA" if has_alpha else "RGB")
        prepared.save(target, "WEBP", quality=80, method=4, exact=has_alpha)

    return before, target.stat().st_size


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    products = [*CATALOG_PRODUCTS, *REFRESCOS_PRODUCTS]
    original_bytes = 0
    mobile_bytes = 0
    for product in products:
        before, after = build_image(product)
        original_bytes += before
        mobile_bytes += after
    reduction = 100 - (mobile_bytes / original_bytes * 100)
    print(
        f"Built {len(products)} images: "
        f"{original_bytes / 1_048_576:.1f} MB -> {mobile_bytes / 1_048_576:.1f} MB "
        f"({reduction:.1f}% smaller)."
    )


if __name__ == "__main__":
    main()
