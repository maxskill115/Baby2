"""Convert the missing-stem originals (backed up on G:) to WebP with the
user's tool defaults (quality 80, longest edge 1600px), complete the checked
set on G:, and refresh Baby2's display files (same names => story/manifest
stay in sync). Original source files are deleted ONLY after their WebP is
verified on G: and in display; failures are left in place.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "Baby2" / "data" / "media-import-audit.json"
G_CHECKED = Path(r"G:\Uncheck\img\WEBP\Cá\IMG_checked")
G_FULLDATA = Path(r"G:\Uncheck\img\FullData\IMG_Lọc\Cá")
DISPLAY = ROOT / "Baby2" / "assets" / "y-khue" / "images"
LOG = ROOT / "Baby2" / "data" / "reconvert-missing-audit.json"
QUALITY = 80
MAX_EDGE = 1600


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def dhash(path: Path) -> str:
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im).convert("L").resize((9, 8))
        pixels = list(im.getdata())
    bits = [pixels[y * 9 + x] > pixels[y * 9 + x + 1] for y in range(8) for x in range(8)]
    return "".join("1" if bit else "0" for bit in bits)


def distance(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right))


def convert(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")
        if max(image.size) > MAX_EDGE:
            image.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        image.save(destination, "WEBP", quality=QUALITY, method=6)


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    g_checked_stems = {p.stem for p in G_CHECKED.rglob("*.webp")}
    decisions_path = ROOT / "Baby2" / "data" / "collision-decisions.json"
    decisions_map = {}
    if decisions_path.exists():
        decisions_map = {g["destination"]: g.get("variants", [])
                         for g in json.loads(decisions_path.read_text(encoding="utf-8")).get("groups", [])}
    display_rows = [r for r in audit["display"]
                    if r["status"] in ("existing", "resolved", "rendered", "pending-collision")]

    # nhóm display cần chuyển: stem chưa có trong checked set của người dùng
    def jobs_for(row):
        jobs = [(row["destination"], row.get("selected") or row["candidates"][0])]
        for variant in row.get("variants", []):
            jobs.append((variant["destination"], variant["source"]))
        for variant in decisions_map.get(row["destination"], []):
            if variant["destination"] not in {j[0] for j in jobs}:
                jobs.append((variant["destination"], variant["source"]))
        return jobs

    # chỉ giữ những row còn ít nhất một destination chưa có ở cả display lẫn checked
    todo = []
    for row in display_rows:
        jobs = jobs_for(row)
        pending_jobs = []
        for dest_rel, source_rel in jobs:
            display_path = ROOT / dest_rel
            checked_path = G_CHECKED / dest_rel.replace("Baby2/assets/y-khue/images/", "")
            if not (display_path.exists() and checked_path.exists()):
                pending_jobs.append((dest_rel, source_rel))
        if pending_jobs:
            todo.append((row, pending_jobs))

    by_source = {row["source"]: row for row in audit["files"]}
    g_files = {}
    for p in G_FULLDATA.rglob("*"):
        if p.is_file():
            g_files.setdefault(p.name, []).append(p)

    converted, deleted, failed = [], [], []
    for row, jobs in todo:
        stem_outputs = []
        ok_all = True
        for dest_rel, source_rel in jobs:
            match = None
            src_row = by_source.get(source_rel)
            if src_row is None:
                # fallback: 24 file legacy-baby1 — bản webp thật nằm ở G:/Uncheck/img/WEBP/Yên
                yen_root = Path("G:/Uncheck/img/WEBP/Yên")
                legacy_candidates = list(yen_root.rglob(Path(source_rel).name))
                if len(legacy_candidates) == 1:
                    src_row = {"bytes": legacy_candidates[0].stat().st_size,
                               "sha256": sha256(legacy_candidates[0])}
                    g_files[Path(source_rel).name] = legacy_candidates
                else:
                    failed.append({"source": source_rel, "reason": "không có trong audit / Yên"})
                    ok_all = False
                    continue
            candidates = [c for c in g_files.get(Path(source_rel).name, [])
                          if c.stat().st_size == src_row["bytes"]]
            match = None
            for c in candidates:
                if sha256(c) == src_row["sha256"]:
                    match = c
                    break
            if match is None:
                failed.append({"source": source_rel, "reason": "không tìm thấy bản gốc trên G: khớp hash"})
                ok_all = False
                continue
            webp_rel = dest_rel  # giữ nguyên đường dẫn display
            display_path = ROOT / webp_rel
            checked_path = G_CHECKED / webp_rel.replace("Baby2/assets/y-khue/images/", "").replace("/", "\\")
            try:
                if match.suffix.lower() == ".webp":
                    # nguồn đã là WebP người dùng xử lý: giữ nguyên chất lượng, chỉ copy
                    display_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(match, display_path)
                else:
                    convert(match, display_path)
                hash_before = dhash(display_path)
                with Image.open(display_path) as im:
                    im.load()
                checked_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(display_path, checked_path)
                if sha256(checked_path) != sha256(display_path):
                    raise RuntimeError("copy vào checked lệch hash")
                stem_outputs.append((str(display_path.relative_to(ROOT)), hash_before))
                converted.append({"source_on_g": str(match), "display": webp_rel,
                                  "checked": str(checked_path), "sha256": sha256(display_path)})
                # ảnh gốc đã có bản WebP verify cả hai nơi -> xóa theo yêu cầu
                match.unlink()
                deleted.append(str(match))
            except Exception as error:
                ok_all = False
                failed.append({"source": source_rel, "reason": str(error)})
                if display_path.exists():
                    display_path.unlink()
        # dedupe same-stem nếu cần (hiếm): các -altN đã là ảnh khác nội dung theo review
        if stem_outputs and ok_all:
            base_hash = stem_outputs[0][1]
            for rel, image_hash in stem_outputs[1:]:
                if distance(base_hash, image_hash) <= 8:
                    print(f"[note] {rel}: trùng nội dung với ảnh chính, giữ lại để review")

    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps({"converted": converted, "deleted_originals": deleted,
                               "failed": failed}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"converted: {len(converted)} | deleted originals: {len(deleted)} | failed: {len(failed)}")
    for f in failed[:10]:
        print("FAILED:", f)


if __name__ == "__main__":
    main()
