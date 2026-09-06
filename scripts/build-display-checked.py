"""Checked-first display build for Baby2.

User-processed set at G:/Uncheck/img/WEBP/Cá (IMG_checked WebP + Video_checked
MP4) is the display source of truth. Originals under assets/y-khue/originals
only fill stems the user's set does not cover; visually distinct same-stem
variants still get -altN files via the reviewed collision flow.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKED = Path(r"G:\Uncheck\img\WEBP\Cá")
ASSETS = ROOT / "Baby2" / "assets" / "y-khue"
AUDIT = ROOT / "Baby2" / "data" / "media-display-checked-audit.json"
DATE_FIX = {"2022-15-08": "2022-08-15"}

spec = importlib.util.spec_from_file_location("import_y_khue", ROOT / "Baby2" / "scripts" / "import-y-khue-media.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
# The shared module persists its own audit file; keep it untouched when we
# borrow build_images/resolve_collisions for the missing-stem subset.
mod.save_audit = lambda audit: None


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def corrected(name: str) -> str:
    prefix = name[:10]
    return DATE_FIX.get(prefix, prefix)


def ym(stem: str) -> Path:
    return Path(corrected(stem)[:4]) / corrected(stem)[5:7]


def copy_checked() -> tuple[list[dict], list[dict]]:
    image_rows, video_rows = [], []
    for source in sorted((CHECKED / "IMG_checked").rglob("*.webp")):
        stem = source.stem
        if not re.match(r"\d{4}-\d{2}-\d{2}", corrected(stem)):
            raise SystemExit(f"Checked image without parsable date: {source}")
        dest = ASSETS / "images" / ym(stem) / f"{stem}.webp"
        group = "digestion" if source.parent.name == "0_consipation" else "camera-checked"
        image_rows.append(entry(source, dest, group))
    for source in sorted((CHECKED / "Video_checked").rglob("*.mp4")):
        stem = source.stem
        if not re.match(r"\d{4}-\d{2}-\d{2}", corrected(stem)):
            raise SystemExit(f"Checked video without parsable date: {source}")
        dest = ASSETS / "videos" / ym(stem) / f"{stem}.mp4"
        video_rows.append(entry(source, dest, "video-checked"))
    return image_rows, video_rows


def entry(source: Path, dest: Path, group: str) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    status = "copied"
    if dest.exists():
        status = "existing" if sha256(dest) == sha256(source) else "content-conflict"
        if status == "content-conflict":
            raise RuntimeError(f"Display conflict with different content: {dest}")
    else:
        shutil.copy2(source, dest)
        if sha256(dest) != sha256(source):
            raise RuntimeError(f"Checksum mismatch after copy: {dest}")
    return {"source": str(source), "destination": dest.relative_to(ROOT).as_posix(), "sha256": sha256(dest), "group": group, "status": status}


def main() -> None:
    audit = mod.load_audit()
    rows = audit["files"]
    g_images = {p.stem for p in (CHECKED / "IMG_checked").rglob("*.webp")}
    image_rows, video_rows = copy_checked()
    # Stems the user's checked set does not cover: render from originals with
    # the existing builder, then keep visually distinct variants via decisions.
    missing = [row for row in rows if row["kind"] == "images" and Path(row["originalFilename"]).stem not in g_images]
    scratch = {"files": missing}
    mod.build_images(missing, scratch)
    mod.make_collision_decisions(scratch)
    mod.resolve_collisions(missing, scratch)
    report = {
        "version": 1,
        "checkedRoot": str(CHECKED),
        "checkedImages": image_rows,
        "checkedVideos": video_rows,
        "missingStemDisplay": scratch.get("display", []),
    }
    AUDIT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    variants = sum(1 for row in report["missingStemDisplay"] if row["status"] == "resolved" for _ in row.get("variants", []))
    print(f"Checked display: {len(image_rows)} images + {len(video_rows)} videos; missing-stem groups: {len(report['missingStemDisplay'])}; variants: {variants}")


if __name__ == "__main__":
    main()
