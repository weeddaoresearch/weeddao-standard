import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
"""Fetch exact COA source URLs; cache text only."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from common import CACHE, FETCH_TIMEOUT, UA, html_to_text

CACHE.mkdir(parents=True, exist_ok=True)


def _safe_name(case_id: str, url: str) -> str:
    host = urlparse(url).netloc.replace(":", "_")
    return re.sub(r"[^A-Za-z0-9._-]+", "_", f"{case_id}_{host}")[:100]


def fetch_url(case_id: str, url: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "case_id": case_id,
        "url": url,
        "ok": False,
        "status": None,
        "kind": "unknown",
        "text": "",
        "html": None,
        "cache_text": None,
        "error": None,
    }
    if case_id in ("COA-001", "COA-002", "COA-003"):
        result.update({"ok": True, "kind": "seed", "status": 200})
        return result

    safe = _safe_name(case_id, url)
    raw_path = CACHE / f"{safe}.bin"
    txt_path = CACHE / f"{safe}.txt"

    cookie_args: list[str] = []
    if "opencoa.org" in url:
        cookie_args = ["-b", "age_verified=1"]

    cmd = [
        "curl", "-sL", "-A", UA, "--max-time", str(FETCH_TIMEOUT),
        "-o", str(raw_path), "-w", "%{http_code}",
        *cookie_args, url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=FETCH_TIMEOUT + 15)
        status = int((proc.stdout or "0").strip() or "0")
        result["status"] = status
        if status != 200 or not raw_path.exists() or raw_path.stat().st_size < 100:
            result["error"] = f"HTTP {status} or empty body"
            return result

        magic = raw_path.read_bytes()[:5]
        is_pdf = magic.startswith(b"%PDF") or url.lower().endswith(".pdf") or ".pdf?" in url.lower()

        if is_pdf:
            result["kind"] = "pdf"
            pdf_path = CACHE / f"{safe}.pdf"
            if raw_path != pdf_path:
                raw_path.replace(pdf_path)
            subprocess.run(
                ["pdftotext", "-layout", str(pdf_path), str(txt_path)],
                capture_output=True, timeout=60,
            )
            # do not keep PDF binary for commit safety — delete after text extract
            try:
                pdf_path.unlink(missing_ok=True)
            except Exception:
                pass
            if txt_path.exists():
                result["text"] = txt_path.read_text(encoding="utf-8", errors="ignore")
        else:
            result["kind"] = "html"
            html = raw_path.read_text(encoding="utf-8", errors="ignore")
            result["html"] = html
            text = html_to_text(html)
            txt_path.write_text(text, encoding="utf-8")
            result["text"] = text
            # keep compact html copy only if needed for OpenCOA structure
            html_path = CACHE / f"{safe}.html"
            html_path.write_text(html, encoding="utf-8")
            try:
                raw_path.unlink(missing_ok=True)
            except Exception:
                pass

        result["cache_text"] = str(txt_path)
        result["ok"] = bool((result.get("text") or "").strip())
        if not result["ok"]:
            result["error"] = "empty text after extraction"
        return result
    except Exception as e:
        result["error"] = str(e)
        return result
