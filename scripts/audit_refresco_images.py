"""Audit drink catalog assets and build a labeled visual contact sheet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "frontend" / "assets" / "refrescos"


def image_metrics(path: Path) -> dict:
    with Image.open(path) as source:
        rgba = source.convert("RGBA")
        alpha = rgba.getchannel("A")
        image = source.convert("RGB")
        grayscale = image.convert("L")
        # Variance after a 4x reduction is a useful warning for soft/upscaled art.
        reduced = grayscale.resize(
            (max(1, image.width // 4), max(1, image.height // 4)),
            Image.Resampling.BOX,
        )
        restored = reduced.resize(image.size, Image.Resampling.BICUBIC)
        difference = ImageStat.Stat(ImageChops.difference(grayscale, restored)).mean[0]
        return {
            "sku": path.stem,
            "width": image.width,
            "height": image.height,
            "bytes": path.stat().st_size,
            "alpha_min": alpha.getextrema()[0],
            "alpha_bbox": alpha.getbbox(),
            "detail_score": round(difference, 2),
        }


def build_sheet(paths: list[Path], target: Path) -> None:
    tile_width, tile_height = 220, 250
    columns = 8
    rows = (len(paths) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * tile_width, rows * tile_height), "#ece8e5")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=18)

    for index, path in enumerate(paths):
        x = (index % columns) * tile_width
        y = (index // columns) * tile_height
        with Image.open(path) as source:
            image = source.convert("RGBA")
            image.thumbnail((190, 205), Image.Resampling.LANCZOS)
            image_x = x + (tile_width - image.width) // 2
            image_y = y + 8 + (205 - image.height) // 2
            canvas.paste(image, (image_x, image_y), image)
        draw.text((x + 12, y + 222), path.stem, fill="#241d20", font=font)

    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, "PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset-dir", type=Path, default=ASSET_DIR)
    parser.add_argument("--sheet", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    paths = sorted(path for path in args.asset_dir.glob("*.webp") if path.is_file() and path.stat().st_size)
    rows = [image_metrics(path) for path in paths]
    if args.sheet:
        build_sheet(paths, args.sheet)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
