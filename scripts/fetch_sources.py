#!/usr/bin/env python3
"""Download selected image URLs and preserve provenance. Requires Pillow.

uv run --with pillow python fetch_sources.py sources.input.json --out research --sheet
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageOps

MAX_BYTES = 25 * 1024 * 1024
EXTENSIONS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "TIFF": ".tif", "GIF": ".gif"}


def read_specs(path: Path) -> list[dict]:
    specs = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(specs, list) or not specs:
        raise ValueError("Input must be a nonempty JSON array.")
    seen = set()
    for item in specs:
        if not isinstance(item, dict):
            raise ValueError("Every source must be an object.")
        source_id = item.get("id", "")
        if not isinstance(source_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", source_id):
            raise ValueError("Each id must use lowercase letters, digits or hyphens (1–64 chars).")
        if source_id in seen:
            raise ValueError(f"Duplicate id: {source_id}")
        seen.add(source_id)
        for key in ("element", "credit", "license"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f"Missing {key} for {source_id}.")
        for key in ("source_page", "image_url"):
            url = item.get(key, "")
            if not isinstance(url, str):
                raise ValueError(f"Invalid {key} for {source_id}.")
            parts = urlsplit(url)
            if parts.scheme not in ("https", "http") or not parts.hostname or parts.username or parts.password:
                raise ValueError(f"{key} must be a public HTTP(S) URL without credentials.")
    return specs


def download(spec: dict, out: Path) -> dict:
    row = dict(spec)
    row["retrieved_at_utc"] = datetime.now(timezone.utc).isoformat()
    try:
        request = Request(spec["image_url"], headers={"User-Agent": "VintageCollageResearch/1.0", "Accept": "image/*"})
        with urlopen(request, timeout=45) as response:
            payload = response.read(MAX_BYTES + 1)
            row["resolved_url"] = response.url
            row["content_type"] = response.headers.get_content_type()
        if len(payload) > MAX_BYTES:
            raise ValueError("Image exceeds 25 MiB; select a smaller source.")
        with Image.open(io.BytesIO(payload)) as im:
            fmt = im.format
            im.verify()
        if fmt not in EXTENSIONS:
            raise ValueError(f"Unsupported format: {fmt}")
        with Image.open(io.BytesIO(payload)) as im:
            width, height = im.size
        relative = Path("assets") / f"{spec['id']}{EXTENSIONS[fmt]}"
        destination = out / relative
        with destination.open("xb") as handle:
            handle.write(payload)
        row.update(status="ok", file=relative.as_posix(), format=fmt,
                   width=width, height=height, bytes=len(payload),
                   sha256=hashlib.sha256(payload).hexdigest(), visual_review="pending")
        print(f"OK {spec['id']}: {width}x{height}, {len(payload)} bytes")
    except Exception as exc:
        row.update(status="error", error=f"{type(exc).__name__}: {exc}")
        print(f"FAIL {spec['id']}: {row['error']}", file=sys.stderr)
    return row


def make_sheet(rows: list[dict], out: Path) -> None:
    good = [r for r in rows if r["status"] == "ok"]
    if not good:
        return
    columns = min(3, len(good))
    cell_w, cell_h = 720, 690
    sheet = Image.new("RGB", (columns * cell_w, ((len(good) + columns - 1) // columns) * cell_h), "#e9e3d8")
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(good):
        x, y = (i % columns) * cell_w, (i // columns) * cell_h
        with Image.open(out / row["file"]) as im:
            thumb = ImageOps.contain(ImageOps.exif_transpose(im).convert("RGB"), (cell_w - 24, cell_h - 50))
            sheet.paste(thumb, (x + (cell_w - thumb.width) // 2, y + 10 + (cell_h - 50 - thumb.height) // 2))
        draw.text((x + 12, y + cell_h - 27), f"{i+1}. {row['id']}  {row['width']}x{row['height']}", fill="black")
    sheet.save(out / "source-contact-sheet.jpg", quality=92)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--sheet", action="store_true")
    args = parser.parse_args()
    specs = read_specs(args.sources)
    manifest = args.out / "sources.manifest.json"
    if manifest.exists():
        raise ValueError("Output already has a manifest; choose a fresh output directory.")
    args.out.mkdir(parents=True, exist_ok=True)
    assets = args.out / "assets"
    if assets.exists() and any(assets.iterdir()):
        raise ValueError("Output assets directory is not empty; choose a fresh output directory.")
    assets.mkdir(exist_ok=True)
    rows = [download(spec, args.out) for spec in specs]
    report = {"schema_version": 1, "note": "Source metadata is supplied by the researcher, not verified by this script.", "sources": rows}
    with manifest.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    if args.sheet:
        make_sheet(rows, args.out)
    return 0 if all(r["status"] == "ok" for r in rows) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
