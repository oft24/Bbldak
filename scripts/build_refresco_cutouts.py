"""Build lightweight transparent drink cut-outs for the hero carousel."""

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import time

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "frontend" / "assets" / "refrescos"
OUTPUT_DIR = SOURCE_DIR / "cutouts"
MAX_SIZE = 1000
MASK_SIZE = 420
BACKGROUND_THRESHOLD = 18


def background_mask(image: Image.Image) -> Image.Image:
    """Return a soft alpha mask while preserving white details inside products."""
    output_size = image.size
    flooded = image.convert("RGB")
    flooded.thumbnail((MASK_SIZE, MASK_SIZE), Image.Resampling.LANCZOS)
    marker = (1, 2, 3)
    ImageDraw.floodfill(flooded, (0, 0), marker, thresh=BACKGROUND_THRESHOLD)

    marker_layer = Image.new("RGB", flooded.size, marker)
    difference = ImageChops.difference(flooded, marker_layer)
    strongest_channel = ImageChops.lighter(
        ImageChops.lighter(difference.getchannel("R"), difference.getchannel("G")),
        difference.getchannel("B"),
    )
    mask = strongest_channel.point(lambda value: 0 if value == 0 else 255)
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    return mask.resize(output_size, Image.Resampling.LANCZOS)


def build_cutout(source: Path, destination: Path) -> None:
    image = Image.open(source).convert("RGBA")
    image.thumbnail((MAX_SIZE, MAX_SIZE), Image.Resampling.LANCZOS)
    detected_background = background_mask(image)
    image.putalpha(ImageChops.multiply(image.getchannel("A"), detected_background))
    destination.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(4):
        try:
            image.save(destination, "WEBP", quality=88, method=4, alpha_quality=100)
            break
        except OSError:
            if attempt == 3:
                raise
            time.sleep(0.2 * (attempt + 1))


def build_source(source: Path) -> None:
    build_cutout(source, OUTPUT_DIR / source.name)


def main() -> None:
    sources = sorted(path for path in SOURCE_DIR.glob("*.webp") if path.is_file())
    with ProcessPoolExecutor(max_workers=4) as pool:
        list(pool.map(build_source, sources))
    print(f"Built {len(sources)} carousel cut-outs in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
