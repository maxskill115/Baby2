"""Resumable, auditable import for Tsàn Ý Khuê's media.

Run from repository root. Every operation is idempotent: a matching destination
hash is skipped, and a different hash stops the batch instead of overwriting.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import subprocess
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Baby2" / "Cá"
ASSETS = ROOT / "Baby2" / "assets" / "y-khue"
AUDIT = ROOT / "Baby2" / "data" / "media-import-audit.json"
IMAGE_EXTENSIONS = {".heic", ".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mov", ".mp4"}
SOURCE_FOLDERS = {"IMG": "camera", "IMG_checked": "checked", "video-ca": "camera"}
DATE_FIXES = {"2022-15-08": "2022-08-15"}


def checksum(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def corrected_date(filename: str) -> str | None:
    prefix = filename[:10]
    if prefix in DATE_FIXES:
        return DATE_FIXES[prefix]
    try:
        return dt.date.fromisoformat(prefix).isoformat()
    except ValueError:
        return None


def source_files():
    for source_name in SOURCE_FOLDERS:
        folder = SOURCE / source_name
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*")):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
                yield source_name, path
    legacy = ROOT / "Baby2" / "assets" / "baby2" / "images"
    if legacy.exists():
        for path in sorted(legacy.rglob("*")):
            if path.is_file() and path.suffix.lower() == ".webp":
                yield "legacy-baby1", path


def original_destination(source_name: str, path: Path, kind: str, date: str | None) -> Path:
    period = Path(*(date.split("-")[:2])) if date else Path("pending-date")
    return ASSETS / "originals" / kind / source_name / period / path.name


def display_filename(path: Path, date: str | None) -> str:
    stem = path.stem
    if path.name[:10] in DATE_FIXES:
        stem = DATE_FIXES[path.name[:10]] + path.name[10:path.name.rfind(".")]
    return stem + ".webp"


def display_destination(path: Path, date: str | None) -> Path:
    period = Path(*(date.split("-")[:2])) if date else Path("pending-date")
    return ASSETS / "images" / period / display_filename(path, date)


def load_audit() -> dict:
    if AUDIT.exists():
        return json.loads(AUDIT.read_text(encoding="utf-8"))
    return {"version": 1, "profile": "y-khue", "dateFixes": DATE_FIXES, "files": [], "display": []}


def save_audit(audit: dict) -> None:
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def inventory() -> list[dict]:
    rows = []
    for source_name, path in source_files():
        ext = path.suffix.lower()
        kind = "images" if ext in IMAGE_EXTENSIONS else "videos"
        date = corrected_date(path.name)
        rows.append({
            "source": relative(path), "sourceName": source_name, "kind": kind,
            "originalFilename": path.name, "date": date, "bytes": path.stat().st_size,
            "sha256": checksum(path), "originalDestination": relative(original_destination(source_name, path, kind, date)),
            "displayDestination": relative(display_destination(path, date)) if kind == "images" else None,
        })
    return rows


def verify_or_move(source: Path, destination: Path, expected_hash: str, move: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if checksum(destination) != expected_hash:
            raise RuntimeError(f"Collision with different content: {destination}")
        return
    if not move:
        return
    shutil.move(str(source), str(destination))
    if checksum(destination) != expected_hash:
        raise RuntimeError(f"Checksum mismatch after move: {destination}")


def import_originals(rows: list[dict], move: bool) -> None:
    for row in rows:
        source = ROOT / row["source"]
        destination = ROOT / row["originalDestination"]
        if source.exists():
            verify_or_move(source, destination, row["sha256"], move)
        elif not destination.exists() or checksum(destination) != row["sha256"]:
            raise RuntimeError(f"Missing source and destination: {row['source']}")


def dhash(path: Path) -> str:
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im).convert("L").resize((9, 8))
        pixels = list(im.getdata())
    bits = [pixels[y * 9 + x] > pixels[y * 9 + x + 1] for y in range(8) for x in range(8)]
    return "".join("1" if bit else "0" for bit in bits)


def distance(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right))


def build_images(rows: list[dict], audit: dict) -> None:
    images = [row for row in rows if row["kind"] == "images"]
    by_dest: dict[str, list[dict]] = defaultdict(list)
    for row in images:
        by_dest[row["displayDestination"]].append(row)
    def render_one(entry: tuple[str, list[dict]]) -> dict:
        dest_rel, candidates = entry
        candidate_hashes = []
        for row in candidates:
            original = ROOT / row["originalDestination"]
            candidate_hashes.append((row, dhash(original)))
        priority = {"IMG_checked": 0, "legacy-baby1": 1, "IMG": 2}
        candidate_hashes.sort(key=lambda entry: priority.get(entry[0]["sourceName"], 9))
        selected, selected_hash = candidate_hashes[0]
        mismatched = [row["source"] for row, image_hash in candidate_hashes[1:] if distance(selected_hash, image_hash) > 8]
        if mismatched:
            return {"destination": dest_rel, "status": "pending-collision", "candidates": [row["source"] for row, _ in candidate_hashes], "mismatched": mismatched}
        destination = ROOT / dest_rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            try:
                with Image.open(destination) as image:
                    image.load()
                return {"destination": dest_rel, "status": "existing", "selected": selected["source"]}
            except Exception:
                destination.unlink()
        source = ROOT / selected["originalDestination"]
        temporary = destination.with_name(destination.name + ".tmp")
        with Image.open(source) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGB")
            image.save(temporary, "WEBP", quality=84, method=6)
        temporary.replace(destination)
        return {"destination": dest_rel, "status": "rendered", "selected": selected["source"], "sources": [row["source"] for row, _ in candidate_hashes]}

    with ThreadPoolExecutor(max_workers=4) as pool:
        rendered = list(pool.map(render_one, sorted(by_dest.items())))
    audit["display"] = rendered
    save_audit(audit)


DECISIONS = ROOT / "Baby2" / "data" / "collision-decisions.json"
VARIANT_SUBTYPES = {
    "Baby2/assets/y-khue/images/2022/12/2022-12-09.webp": "screenshot-of-selected-photo",
    "Baby2/assets/y-khue/images/2023/03/2023-03-17.webp": "screenshot-of-selected-photo",
    "Baby2/assets/y-khue/images/2023/03/2023-03-17_1.webp": "screenshot/crop-of-selected-photo",
}


def load_decisions() -> dict:
    if not DECISIONS.exists():
        raise SystemExit("Missing collision-decisions.json; run make-collision-decisions first")
    return json.loads(DECISIONS.read_text(encoding="utf-8"))


def save_decisions(decisions: dict) -> None:
    DECISIONS.parent.mkdir(parents=True, exist_ok=True)
    DECISIONS.write_text(json.dumps(decisions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_collision_decisions(audit: dict) -> None:
    """Every visually distinct collision candidate becomes its own display file.

    Reviewed 2026-09-06 from Baby2/review/collision-sheets: mismatched
    candidates are different photos (or call/app screenshots), so nothing is
    merged; each keeps content under a deterministic -altN name.
    """
    decisions = {"version": 1, "reviewed": "2026-09-06", "rule": "keep-all-distinct-content", "groups": []}
    for entry in audit["display"]:
        if entry["status"] != "pending-collision":
            continue
        others = sorted(entry["mismatched"])
        variants = []
        for index, source in enumerate(others, start=2):
            row = next(row for row in audit["files"] if row["source"] == source)
            dest = ROOT / entry["destination"]
            variant = dest.with_name(dest.stem + f"-alt{index}.webp")
            variants.append({
                "source": source,
                "destination": relative(variant),
                "subtype": VARIANT_SUBTYPES.get(entry["destination"], "different-photo"),
            })
        decisions["groups"].append({"destination": entry["destination"], "variants": variants})
    save_decisions(decisions)
    print(f"Decisions for {len(decisions['groups'])} collision groups")


def render_webp(original: Path, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        try:
            with Image.open(destination) as image:
                image.load()
            return "existing"
        except Exception:
            destination.unlink()
    temporary = destination.with_name(destination.name + ".tmp")
    with Image.open(original) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")
        image.save(temporary, "WEBP", quality=84, method=6)
    temporary.replace(destination)
    return "rendered"


def resolve_collisions(rows: list[dict], audit: dict) -> None:
    decisions = load_decisions()
    by_source = {row["source"]: row for row in rows}
    resolved = 0
    for group in decisions["groups"]:
        entry = next(row for row in audit["display"] if row["destination"] == group["destination"])
        selected_source = entry["candidates"][0]
        selected_row = by_source[selected_source]
        entry["selected"] = selected_source
        entry["mainStatus"] = render_webp(ROOT / selected_row["originalDestination"], ROOT / entry["destination"])
        variant_rows = []
        for variant in group["variants"]:
            row = by_source[variant["source"]]
            status = render_webp(ROOT / row["originalDestination"], ROOT / variant["destination"])
            variant_rows.append({**variant, "status": status})
            resolved += 1
        entry["status"] = "resolved"
        entry["variants"] = variant_rows
        entry["subtype"] = VARIANT_SUBTYPES.get(group["destination"], "different-photo")
    save_audit(audit)
    print(f"Variant display files processed: {resolved}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("inventory", "move-originals", "build-images", "make-collision-decisions", "resolve-collisions"))
    parser.add_argument("--move", action="store_true", help="Required for moving source files")
    args = parser.parse_args()
    audit = load_audit()
    rows = inventory() if args.action == "inventory" or not audit["files"] else audit["files"]
    if args.action == "inventory":
        audit["files"] = rows
        save_audit(audit)
        print(f"Inventory: {len(rows)} source files")
    elif args.action == "move-originals":
        if not args.move:
            raise SystemExit("Pass --move after reviewing media-import-audit.json")
        import_originals(rows, move=True)
        audit["files"] = rows
        save_audit(audit)
        print(f"Moved and hash-verified: {len(rows)} source files")
    elif args.action == "make-collision-decisions":
        build_images(rows, audit)
        make_collision_decisions(audit)
    elif args.action == "resolve-collisions":
        resolve_collisions(rows, audit)
    else:
        build_images(rows, audit)
        complete = sum(row["status"] in {"rendered", "existing"} for row in audit["display"])
        pending = sum(row["status"] == "pending-collision" for row in audit["display"])
        print(f"Display images: {complete}; pending content collisions: {pending}")


if __name__ == "__main__":
    main()
