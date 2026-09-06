"""Build the Baby2 runtime manifest from rendered display files only."""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "Baby2" / "assets" / "y-khue"
BIRTH = dt.date(2022, 12, 8)


def main() -> None:
    checked_audit = ROOT / "Baby2" / "data" / "media-display-checked-audit.json"
    digestion = set()
    if checked_audit.exists():
        report = json.loads(checked_audit.read_text(encoding="utf-8"))
        digestion = {row["destination"] for row in report.get("checkedImages", []) if row.get("group") == "digestion"}
    items = []
    for kind, suffix in (("images", ".webp"), ("videos", ".mp4")):
        folder = ASSETS / kind
        for path in sorted(folder.rglob(f"*{suffix}")) if folder.exists() else []:
            try:
                date = dt.date.fromisoformat(path.name[:10])
            except ValueError:
                print(f"[manifest] skip (filename needs YYYY-MM-DD prefix): {path.name}", file=sys.stderr)
                continue
            rel = path.relative_to(ROOT / "Baby2").as_posix()
            group = "prenatal" if date < BIRTH else "diary"
            if rel in digestion:
                group = "digestion"
            item = {"id": rel, "src": "./" + rel, "originalFilename": path.name, "date": date.isoformat(),
                    "type": "image" if kind == "images" else "video", "group": group}
            if kind == "videos":
                item["poster"] = "./" + rel.replace("/videos/", "/posters/").rsplit(".", 1)[0] + ".webp"
            items.append(item)
    items.sort(key=lambda item: (item["date"], item["src"]))
    manifest = {"version": 1, "profileId": "y-khue", "items": items,
                "counts": {"images": sum(i["type"] == "image" for i in items), "videos": sum(i["type"] == "video" for i in items),
                           "prenatal": sum(i["group"] == "prenatal" for i in items)}}
    output = ROOT / "Baby2" / "data" / "media-manifest.js"
    output.write_text("window.BABY_MEDIA_MANIFEST = " + json.dumps(manifest, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    print(manifest["counts"])


if __name__ == "__main__":
    main()
