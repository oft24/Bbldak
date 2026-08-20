"""Create production-sized WebP copies of the original showroom PNG assets."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "frontend" / "assets"
SOURCES = [*ASSETS.glob("*.png"), *(ASSETS / "catalog").glob("*.png")]
MAX_EDGE = 1400


def optimize(source: Path) -> tuple[int, int]:
    target = source.with_suffix(".webp")
    with Image.open(source) as raw:
        image = raw.convert("RGBA")
        image.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        image.save(target, "WEBP", quality=86, method=4, exact=True)
    return source.stat().st_size, target.stat().st_size


def main() -> None:
    original = optimized = 0
    for source in SOURCES:
        before, after = optimize(source)
        original += before
        optimized += after
        print(f"{source.name}: {before / 1024:.0f} KB -> {after / 1024:.0f} KB")
    print(f"Total: {original / 1024 / 1024:.1f} MB -> {optimized / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
