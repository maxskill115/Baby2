"""Build browser-safe MP4 display copies from preserved Baby2 originals."""
from __future__ import annotations

import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "Baby2" / "data" / "media-import-audit.json"
ASSETS = ROOT / "Baby2" / "assets" / "y-khue"


def codec(path: Path) -> str:
    result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=nokey=1:noprint_wrappers=1", str(path)], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def build_one(row: dict) -> dict:
    original = ROOT / row["originalDestination"]
    dest = ASSETS / "videos" / row["date"][:4] / row["date"][5:7] / (Path(row["originalFilename"]).stem + ".mp4")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 32:
        return {"source": row["source"], "destination": dest.relative_to(ROOT).as_posix(), "status": "existing"}
    source_codec = codec(original)
    if source_codec == "h264":
        command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(original), "-map", "0:v:0", "-map", "0:a?", "-c", "copy", "-movflags", "+faststart", str(dest)]
        mode = "remux"
    else:
        command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(original), "-map", "0:v:0", "-map", "0:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", str(dest)]
        mode = "transcode"
    temporary = dest.with_name(dest.name + ".tmp")
    subprocess.run(command[:-1] + ["-f", "mp4", str(temporary)], check=True)
    temporary.replace(dest)
    return {"source": row["source"], "destination": dest.relative_to(ROOT).as_posix(), "codec": source_codec, "mode": mode, "status": "built"}


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    rows = [row for row in audit["files"] if row["kind"] == "videos"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        output = list(pool.map(build_one, rows))
    audit["videoDisplay"] = output
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    built = sum(1 for row in output if row["status"] == "built")
    print(f"Browser MP4 complete: {len(output)} ({built} newly built)")


if __name__ == "__main__":
    main()
