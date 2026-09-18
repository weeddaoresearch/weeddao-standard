"""Shared constants and helpers for WeedDAO COA corpus v0.1 build."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CORPUS = ROOT / "corpus" / "v0.1"
INPUTS = CORPUS / "inputs"
CACHE = CORPUS / "cache"
CASES = CORPUS / "cases"
MAPPINGS = CORPUS / "mappings"
REVIEWS = CORPUS / "reviews"
DOCS = ROOT / "docs"
SCHEMA = ROOT / "schemas" / "weeddao-cultivation-record-v0.1-alpha.schema.json"
VALIDATE = ROOT / "scripts" / "validate.py"
PYTHON = Path("/workspace/weeddao/.venv/bin/python")
REVIEW_DATA = ROOT / "review-data"
EXPECTED_SCHEMA_SHA = "31b0bdab4585954bebb9af1b06ac8b2d5a7b513ad1ca9694070836f1c723b5ee"
UA = "WeedDAOCorpusBot/0.1 (+research)"
FETCH_TIMEOUT = 35
WORKERS = 5
CREATED_AT = "2026-09-18T17:00:00Z"
RETRIEVED_AT = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

CANN_KEYS = {
    "thc", "thca", "cbd", "cbda", "cbg", "cbga", "cbc", "cbn", "thcv",
    "total_thc", "total_cbd", "total_cannabinoids",
}

JURISDICTION_MAP = {
    "new mexico": "US-NM",
    "texas": "US-TX",
    "missouri": "US-MO",
    "new york": "US-NY",
    "connecticut": "US-CT",
    "massachusetts": "US-MA",
    "louisiana brand / california lab": "US-CA",
    "louisiana brand": "US-LA",
    "texas retail / oregon laboratory": "US-OR",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def jurisdiction_code(hint: str | None) -> str | None:
    if not hint:
        return None
    h = hint.strip().lower()
    if h in JURISDICTION_MAP:
        return JURISDICTION_MAP[h]
    for k, v in JURISDICTION_MAP.items():
        if k in h:
            return v
    return None


def normalize_cann_name(name: str) -> str | None:
    n = name.lower().strip()
    n = n.replace("−", "-").replace("–", "-").replace("—", "-")
    n = re.sub(r"&delta;?", "delta", n, flags=re.I)
    n = n.replace("δ", "delta").replace("Δ", "delta").replace("∆", "delta")
    n = re.sub(r"\s+", " ", n)
    n = re.sub(r"delta\s*-?\s*9\s*-?\s*thc", "thc", n)
    n = re.sub(r"d\s*9\s*-?\s*thc", "thc", n)
    n = re.sub(r"delta\s*-?\s*8\s*-?\s*thc", "d8thc", n)
    n = n.replace("thc-a", "thca").replace("cbd-a", "cbda").replace("cbg-a", "cbga")
    n = n.replace("thc a", "thca").replace("total thc", "total_thc").replace("total cbd", "total_cbd")
    n = n.replace("total cannabinoids", "total_cannabinoids").replace("sum of cannabinoids", "total_cannabinoids")
    n = n.replace(" ", "_").replace("-", "")
    aliases = {
        "thc": "thc", "d9thc": "thc", "delta9thc": "thc", "thca": "thca",
        "cbd": "cbd", "cbda": "cbda", "cbg": "cbg", "cbga": "cbga",
        "cbc": "cbc", "cbn": "cbn", "thcv": "thcv",
        "total_thc": "total_thc", "totalthc": "total_thc",
        "total_cbd": "total_cbd", "totalcbd": "total_cbd",
        "total_cannabinoids": "total_cannabinoids", "totalcannabinoids": "total_cannabinoids",
    }
    return aliases.get(n)


def parse_numeric_token(tok: str) -> tuple[str, float | None]:
    t = tok.strip().replace(",", "").replace("\xa0", " ")
    tl = t.lower()
    if tl in ("nd", "n.d.", "not detected", "not_detected"):
        return "nd", None
    if tl in ("nt", "not tested", "not_tested", "not performed", "not_performed", "n/t"):
        return "not_tested", None
    if tl in ("nr", "not reported", "not_reported", "n/r"):
        return "not_reported", None
    if re.match(r"^<\s*(loq|lod|lor|rl)\b", tl) or tl.startswith("<loq") or tl.startswith("<lod"):
        return "below_limit", None
    if re.match(r"^<\s*[0-9]", t):
        return "below_limit", None
    m = re.match(r"^([0-9]*\.?[0-9]+)\s*$", t)
    if m:
        return "numeric", float(m.group(1))
    return "unknown", None


def html_to_text(html: str) -> str:
    html = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?i)</(p|div|tr|li|h\d|td|th)>", "\n", html)
    html = re.sub(r"(?i)&nbsp;", " ", html)
    html = re.sub(r"(?i)&lt;", "<", html)
    html = re.sub(r"(?i)&gt;", ">", html)
    html = re.sub(r"(?i)&amp;", "&", html)
    html = re.sub(r"(?i)&delta;", "delta", html)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n+", "\n", html)
    return html


def extract_panel_status(text: str) -> dict[str, str | None]:
    panels = {
        "microbials": None,
        "pesticides": None,
        "heavy_metals": None,
        "residual_solvents": None,
        "mycotoxins": None,
    }

    def norm(s: str) -> str:
        s = s.lower().replace(" ", "_")
        if s.startswith("pass"):
            return "pass"
        if s.startswith("fail"):
            return "fail"
        if "not_tested" in s or "not_performed" in s or s in ("nt", "not_tested"):
            return "not_tested"
        return s

    patterns = [
        (r"(?i)microbial[s]?\s*(?:analysis|testing|panel)?\s*[:\-]?\s*(pass(?:ed)?|fail(?:ed)?|not\s*tested|not\s*performed)", "microbials"),
        (r"(?i)pesticide[s]?\s*(?:analysis|testing|panel)?\s*[:\-]?\s*(pass(?:ed)?|fail(?:ed)?|not\s*tested|not\s*performed)", "pesticides"),
        (r"(?i)heavy\s*metals?\s*(?:analysis|testing|panel)?\s*[:\-]?\s*(pass(?:ed)?|fail(?:ed)?|not\s*tested|not\s*performed)", "heavy_metals"),
        (r"(?i)residual\s*solvents?\s*(?:analysis|testing|panel)?\s*[:\-]?\s*(pass(?:ed)?|fail(?:ed)?|not\s*tested|not\s*performed)", "residual_solvents"),
        (r"(?i)mycotoxin[s]?\s*(?:analysis|testing|panel)?\s*[:\-]?\s*(pass(?:ed)?|fail(?:ed)?|not\s*tested|not\s*performed)", "mycotoxins"),
        (r"(?i)\bMicrobial\s+(Pass|Fail)\b", "microbials"),
        (r"(?i)\bPesticides?\s+(Pass|Fail)\b", "pesticides"),
        (r"(?i)\bHeavy\s+Metals?\s+(Pass|Fail)\b", "heavy_metals"),
        (r"(?i)\bResidual\s+Solvents?\s+(Pass|Fail)\b", "residual_solvents"),
        (r"(?i)\bMycotoxins?\s+(Pass|Fail)\b", "mycotoxins"),
        (r"(?i)\bAdditives\s+(Pass|Fail)\b", None),
        (r"(?i)\bForeign\s+(?:Materials?|Matter)\s+(Pass|Fail)\b", None),
    ]
    for pat, key in patterns:
        if key is None:
            continue
        m = re.search(pat, text)
        if m and panels[key] is None:
            panels[key] = norm(m.group(1))
    return panels


def validate_record(path: Path) -> bool:
    proc = subprocess.run(
        [str(PYTHON), str(VALIDATE), str(path)],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def empty_parsed() -> dict[str, Any]:
    return {
        "cannabinoids": {},
        "terpenes": [],
        "nd_cannabinoids": [],
        "below_limit_cannabinoids": [],
        "nd_terpenes": [],
        "below_limit_terpenes": [],
        "multi_unit": False,
        "meta": {},
        "panels": {
            "microbials": None,
            "pesticides": None,
            "heavy_metals": None,
            "residual_solvents": None,
            "mycotoxins": None,
        },
        "moisture": None,
        "water_activity": None,
        "foreign_material": None,
    }
