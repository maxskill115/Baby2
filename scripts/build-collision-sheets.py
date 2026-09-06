"""Render pending-collision candidates side by side for visual review.

Each pending destination from media-import-audit.json gets a strip showing
every candidate original (source-mapped), labelled with its source folder,
so same-name/different-content groups can be classified during review.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw
import pillow_heif

pillow_heif.register_heif_opener()

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "Baby2" / "data" / "media-import-audit.json"
OUT = ROOT / "Baby2" / "review" / "collision-sheets"

audit = json.loads(AUDIT.read_text(encoding="utf-8"))
by_source = {row["source"]: row for row in audit["files"]}
pending = [row for row in audit["display"] if row["status"] == "pending-collision"]

cols, cell_w, cell_h = 4, 300, 260
strip_w = cols * cell_w
rows_per_page = 5
per_page = rows_per_page

for page in range(math.ceil(len(pending) / per_page)):
    batch = pending[page * per_page:(page + 1) * per_page]
    canvas = Image.new("RGB", (strip_w, len(batch) * cell_h), "white")
    draw = ImageDraw.Draw(canvas)
    for row_index, entry in enumerate(batch):
        y = row_index * cell_h
        dest_name = entry["destination"].replace("Baby2/assets/y-khue/images/", "")
        draw.text((6, y + 4), f"[{page * per_page + row_index}] {dest_name}", fill="#B3261E")
        for col_index, source_rel in enumerate(entry["candidates"]):
            row = by_source.get(source_rel)
            original = ROOT / row["originalDestination"] if row else ROOT / source_rel
            x = col_index * cell_w
            tag = "?"
            if row:
                tag = row["sourceName"]
                if source_rel in entry.get("mismatched", []):
                    tag += " DIFF"
            try:
                with Image.open(original) as image:
                    image = __import__("PIL.ImageOps", fromlist=["exif_transpose"]).exif_transpose(image)
                    image.thumbnail((cell_w - 10, cell_h - 40))
                    canvas.paste(image.convert("RGB"), (x + 5, y + 22))
            except Exception as error:
                draw.text((x + 5, y + 40), f"ERR {error}", fill="#B3261E")
            draw.text((x + 5, y + cell_h - 16), f"{col_index}:{tag} {original.name[:34]}", fill="#243D33")
    dest = OUT / f"{page:03d}.jpg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, quality=88)
    print(f"{dest.name}: {len(batch)} collisions")

print(f"total pending: {len(pending)}")
