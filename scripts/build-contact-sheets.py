"""Create review contact sheets from Baby2 display images and video posters."""
from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Baby2" / "review" / "contact-sheets"


def sheet(paths: list[Path], label: str) -> None:
    cols, cell_w, cell_h = 6, 220, 180
    for page in range(math.ceil(len(paths) / 36)):
        batch = paths[page * 36:(page + 1) * 36]
        image = Image.new("RGB", (cols * cell_w, math.ceil(len(batch) / cols) * cell_h), "white")
        draw = ImageDraw.Draw(image)
        for index, path in enumerate(batch):
            with Image.open(path) as source:
                source.thumbnail((cell_w - 10, cell_h - 35))
                x, y = (index % cols) * cell_w, (index // cols) * cell_h
                image.paste(source.convert("RGB"), (x + 5, y + 4))
                draw.text((x + 5, y + cell_h - 28), path.name[:31], fill="#243D33")
        dest = OUT / label / f"{page:03d}.jpg"
        dest.parent.mkdir(parents=True, exist_ok=True)
        image.save(dest, quality=86)


for folder, label in ((ROOT / "Baby2" / "assets" / "y-khue" / "images", "images"), (ROOT / "Baby2" / "assets" / "y-khue" / "posters", "videos")):
    paths = sorted(folder.rglob("*.webp")) if folder.exists() else []
    if paths:
        sheet(paths, label)
        print(f"{label}: {len(paths)}")
