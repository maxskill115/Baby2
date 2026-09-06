"""Baby2 browser smoke test: gate -> journey -> media rules.

Checks: no JS errors, no failed requests (404), no premature MP4 requests,
album opens, video plays only after click, at 1440x900 and 390x844.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/Baby2/"
PASSWORD = "".join(chr(n ^ 91) for n in [109, 106, 106, 104, 107, 107])


def run(viewport: dict) -> dict:
    js_errors, failed, mp4_early = [], [], []
    report = {"viewport": viewport, "jsErrors": js_errors, "failedRequests": failed, "earlyMp4": mp4_early}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_context(viewport=viewport).new_page()
        page.on("pageerror", lambda e: js_errors.append(str(e)))
        page.on("requestfailed", lambda r: failed.append(r.url))
        page.on("response", lambda r: failed.append(f"{r.status} {r.url}") if r.status >= 400 else None)
        page.on("request", lambda r: mp4_early.append(r.url) if ".mp4" in r.url and r.resource_type in ("media", "fetch", "xhr") else None)
        page.goto(BASE, wait_until="networkidle")

        page.fill("#babyAccessInput", PASSWORD)
        page.click("#babyAccessSubmit")
        page.wait_for_selector("#journeyStream", timeout=20000)
        page.wait_for_timeout(2500)

        summary = page.evaluate("""() => ({
            scenes: document.querySelectorAll('#journeyStream > *').length,
            mediaSummary: window.BABY_DISCOVERY_DATA ? (window.BABY_MEDIA_MANIFEST || {counts:{}}).counts : null,
            profileName: document.getElementById('profileName')?.textContent,
            digestTitle: Array.from(document.querySelectorAll('strong,h2,h3')).some(el => el.textContent.includes('Ý Khuê')),
            yenLeak: document.body.innerText.includes('Thúy Yên')
        })""")
        report["summary"] = summary

        albums = page.query_selector_all("[data-open-gallery]")
        report["albumButtons"] = len(albums)
        with_video = [a for a in albums if "video" in (a.text_content() or "")]
        target = (with_video or albums)
        if target:
            pick = target[min(2, len(target) - 1)]
            pick.scroll_into_view_if_needed()
            page.wait_for_timeout(800)
            pick.click()
            page.wait_for_timeout(1500)
            page.mouse.wheel(0, 600)
            page.wait_for_timeout(2500)
            thumbs = page.query_selector_all("[data-open-media]")
            report["thumbsInAlbum"] = len(thumbs)
            report["thumbsLoaded"] = sum(1 for t in thumbs if t.query_selector("img") and t.query_selector("img").evaluate("el => el.naturalWidth > 0"))
            videos = [t for t in thumbs if t.get_attribute("data-media-kind") == "video"]
            report["videoThumbs"] = len(videos)
            if videos:
                videos[0].scroll_into_view_if_needed()
                page.wait_for_timeout(600)
                mp4_before_click = len(mp4_early)
                videos[0].click()
                page.wait_for_timeout(2500)
                report["videoOpened"] = bool(page.query_selector("video"))
                report["playingVideos"] = page.evaluate("() => Array.from(document.querySelectorAll('video')).filter(v => !v.paused).length")
                report["earlyMp4"] = mp4_early[:mp4_before_click]
        page.screenshot(path=str(ROOT / "Baby2" / "review" / f"smoke-{viewport['width']}.png"), full_page=False)
        browser.close()
    report["ok"] = not js_errors and not failed and not report["earlyMp4"]
    return report


results = [run({"width": 1440, "height": 900}), run({"width": 390, "height": 844})]
out = ROOT / "Baby2" / "review" / "smoke-report.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, ensure_ascii=False, indent=2))
