"""Best-effort COA text parsers (TagLeaf, OpenCOA, generic PDF). Never invent numbers."""
from __future__ import annotations

import re
from typing import Any

from common import empty_parsed, extract_panel_status, normalize_cann_name, parse_numeric_token


def _set_cann(out: dict, key: str, kind: str, value: float | None, unit: str = "%", alt: dict | None = None):
    if kind == "numeric" and value is not None:
        if key in out["cannabinoids"] and out["cannabinoids"][key].get("kind") == "numeric":
            return
        entry = {"kind": "numeric", "value": value, "unit": unit, "alt": alt or {}}
        out["cannabinoids"][key] = entry
        if alt:
            out["multi_unit"] = True
    elif kind == "nd":
        if key not in out["nd_cannabinoids"]:
            out["nd_cannabinoids"].append(key)
    elif kind == "below_limit":
        if key not in out["below_limit_cannabinoids"]:
            out["below_limit_cannabinoids"].append(key)


def parse_tagleaf(text: str) -> dict[str, Any]:
    out = empty_parsed()
    t = text.replace("&Delta;", "Δ").replace("&delta;", "δ")
    for pat, key in [
        (r"Batch No\.\s*:\s*(\S+)", "batch"),
        (r"Sample ID\s*:\s*(\S+)", "sample"),
        (r"Batch Result\s*:\s*(\w+)", "overall"),
        (r"METRC Src Tag\s*:\s*(\S+)", "metrc_src"),
        (r"Metrc Testing Tag\s*:\s*(\S+)", "metrc_test"),
        (r"Client\s*:\s*([^\n/]+)", "client"),
        (r"Matrix\s*:\s*([A-Za-z ]+)", "matrix"),
    ]:
        m = re.search(pat, t)
        if m:
            out["meta"][key] = m.group(1).strip()

    analytes = [
        ("Total THC", "total_thc"), ("Total CBD", "total_cbd"), ("Total Cannabinoids", "total_cannabinoids"),
        ("THCA", "thca"), ("CBGA", "cbga"), ("CBG", "cbg"), ("CBDA", "cbda"), ("CBD", "cbd"),
        ("CBCA", None), ("CBC", "cbc"), ("CBN", "cbn"), ("THCV", "thcv"), ("THCVA", None),
        ("CBDV", None), ("CBDVA", None),
        ("Δ 9 -THC", "thc"), ("Δ9-THC", "thc"), ("Δ 8 -THC", None), ("Δ8-THC", None),
    ]
    for aname, key in analytes:
        for m in re.finditer(re.escape(aname) + r"\s+([^\n]{0,60})", t, re.I):
            snippet = m.group(0)
            if re.search(r"(?i)per\s+(serving|package)", snippet):
                continue
            rest = m.group(1).strip()
            mm = re.match(
                r"(ND|<LOQ|<LOD|<\s*LOQ|<\s*LOD|<\s*[0-9.]+|[0-9]*\.?[0-9]+)\s*%?\s*"
                r"(ND|<LOQ|<LOD|<\s*LOQ|<\s*LOD|<\s*[0-9.]+|[0-9]*\.?[0-9]+)?",
                rest, re.I,
            )
            if not mm:
                continue
            kind_a, val_a = parse_numeric_token(mm.group(1))
            alt = {}
            if mm.group(2):
                kind_b, val_b = parse_numeric_token(mm.group(2))
                if kind_b == "numeric" and val_b is not None:
                    alt["mg/g"] = val_b
            if key is None:
                if kind_a == "nd":
                    out["nd_cannabinoids"].append(aname)
                elif kind_a == "below_limit":
                    out["below_limit_cannabinoids"].append(aname)
            else:
                _set_cann(out, key, kind_a, val_a, "%", alt or None)
            break

    # Terpenes
    mterp = re.search(
        r"Terpenes Testing.*?(?=Heavy Metals|Pesticide|Microbial|Foreign|Residual|Mycotoxin|Results Certified|$)",
        t, re.I | re.S,
    )
    terp_sec = mterp.group(0) if mterp else t
    m = re.search(r"Total Terpenes\s+([0-9]*\.?[0-9]+)\s*%", terp_sec, re.I)
    if m:
        out["meta"]["total_terpenes"] = float(m.group(1))
    for tname in [
        "β -Caryophyllene", "beta-Caryophyllene", "d-Limonene", "Limonene", "Linalool",
        "Nerolidol", "β -Myrcene", "beta-Myrcene", "Myrcene", "α -Bisabolol", "alpha-Bisabolol",
        "α -Humulene", "alpha-Humulene", "Humulene", "Guaiol", "β -Pinene", "beta-Pinene",
        "α -Pinene", "alpha-Pinene", "Camphene", "Terpinolene", "Ocimene", "Geraniol",
        "Eucalyptol", "Valencene", "Fenchol", "Borneol",
    ]:
        m = re.search(re.escape(tname) + r"\s+(ND|<LOQ|<LOD|<\s*LOQ|[0-9]*\.?[0-9]+)", terp_sec, re.I)
        if not m:
            continue
        kind, val = parse_numeric_token(m.group(1))
        display = (
            tname.replace("β -", "beta-").replace("α -", "alpha-")
            .replace("β-", "beta-").replace("α-", "alpha-")
        )
        display = re.sub(r"\s+", " ", display).strip().lower()
        if kind == "numeric" and val is not None:
            if not any(x["name"] == display for x in out["terpenes"]):
                out["terpenes"].append({"name": display, "value": val, "unit": "%"})
        elif kind == "nd":
            out["nd_terpenes"].append(display)
        elif kind == "below_limit":
            out["below_limit_terpenes"].append(display)

    out["panels"] = extract_panel_status(t)
    # TagLeaf summary chips: "Microbial Pass"
    for key, pat in [
        ("microbials", r"(?i)\bMicrobial\s+(Pass|Fail)\b"),
        ("pesticides", r"(?i)\bPesticides?\s+(Pass|Fail)\b"),
        ("heavy_metals", r"(?i)\bHeavy\s+Metals?\s+(Pass|Fail)\b"),
        ("residual_solvents", r"(?i)\bResidual\s+Solvents?\s+(Pass|Fail)\b"),
        ("mycotoxins", r"(?i)\bMycotoxins?\s+(Pass|Fail)\b"),
    ]:
        m = re.search(pat, t)
        if m and not out["panels"].get(key):
            out["panels"][key] = m.group(1).lower()
    if re.search(r"(?i)Foreign\s+Materials?\s+Pass", t):
        out["foreign_material"] = "pass"
    if out["cannabinoids"] and any(v.get("alt") for v in out["cannabinoids"].values()):
        out["multi_unit"] = True
    return out


def parse_opencoa(html: str | None, text: str) -> dict[str, Any]:
    out = parse_generic(text)
    src = html or text
    # Card-style cannabinoids
    for m in re.finditer(
        r"(?is)(Δ9-THC|THC-A|THCA|CBD|CBG|CBDA|Total\s*THC|Total\s*CBD)\s*</span>\s*"
        r"<span[^>]*>\s*([0-9]*\.?[0-9]+)\s*%",
        src,
    ):
        key = normalize_cann_name(m.group(1).replace("THC-A", "THCA"))
        if key:
            _set_cann(out, key, "numeric", float(m.group(2)), "%")
    for m in re.finditer(
        r"(?i)(Δ9-THC|THCA|CBD|CBG|Total\s*THC|Total\s*CBD)\s+([0-9]*\.?[0-9]+)\s*%",
        text,
    ):
        key = normalize_cann_name(m.group(1))
        if key:
            _set_cann(out, key, "numeric", float(m.group(2)), "%")
    # Safety panel Pass headings
    for key, pat in [
        ("microbials", r"(?i)microbials?\s*\([^)]*\)[\s\S]{0,80}?Pass"),
        ("pesticides", r"(?i)pesticides?\s*\([^)]*\)[\s\S]{0,80}?Pass"),
        ("heavy_metals", r"(?i)heavy metals?[\s\S]{0,120}?Pass"),
        ("residual_solvents", r"(?i)residual solvents?\s*\([^)]*\)[\s\S]{0,80}?Pass"),
        ("mycotoxins", r"(?i)mycotoxins?\s*\([^)]*\)[\s\S]{0,80}?Pass"),
    ]:
        if out["panels"].get(key) is None and re.search(pat, text):
            out["panels"][key] = "pass"
    if re.search(r"(?i)Arsenic\s+(ND|Not Detected).{0,40}Pass", text):
        out["panels"]["heavy_metals"] = out["panels"].get("heavy_metals") or "pass"
    return out


def parse_generic(text: str) -> dict[str, Any]:
    out = empty_parsed()
    for pat, key in [
        (r"(?i)Batch\s*(?:Number|No\.?|#)?\s*[:#]?\s*([A-Za-z0-9][A-Za-z0-9._\-/]{1,40})", "batch"),
        (r"(?i)Batch#:\s*([A-Za-z0-9._\-/]+)", "batch"),
        (r"(?i)Sample(?:\s*ID)?\s*[:#]?\s*([A-Za-z0-9][A-Za-z0-9._\-/]{1,40})", "sample"),
        (r"(?i)Lab ID:\s*(\S+)", "sample"),
        (r"(?i)Strain:\s*([^\n]{2,60})", "strain"),
    ]:
        m = re.search(pat, text)
        if m and key not in out["meta"]:
            out["meta"][key] = m.group(1).strip()

    # Summary totals with units
    for label, key in [
        ("Total THC", "total_thc"), ("Total CBD", "total_cbd"),
        ("Total Cannabinoids", "total_cannabinoids"), ("Sum of Cannabinoids", "total_cannabinoids"),
    ]:
        m = re.search(
            rf"(?i){re.escape(label)}\s*[:\s]+([0-9]*\.?[0-9]+)\s*(%|mg/g|mg/mL|mg/ml|mg/serving|mg/unit)?",
            text,
        )
        if m and key not in out["cannabinoids"]:
            raw_u = (m.group(2) or "%").replace("mL", "ml")
            if raw_u.lower() in ("mg/unit",):
                unit = "mg/serving"
            elif raw_u.lower() == "mg/ml":
                unit = "mg/ml"
            elif raw_u.lower() == "mg/g":
                unit = "mg/g"
            else:
                unit = "%"
            _set_cann(out, key, "numeric", float(m.group(1)), unit)

    # Table-like analyte rows (ACT / ChemHistory / Kaycha-ish)
    table_analytes = {
        "THCa": "thca", "THCA": "thca", "D9-THC": "thc", "Δ9-THC": "thc", "d9-THC": "thc",
        "DELTA-9-THC": "thc", "DELTA-9 THC": "thc",
        "CBD": "cbd", "CBDa": "cbda", "CBDA": "cbda", "CBG": "cbg", "CBGa": "cbga", "CBGA": "cbga",
        "CBC": "cbc", "CBN": "cbn", "THCV": "thcv",
        "Total THC": "total_thc", "TOTAL THC": "total_thc",
        "Total CBD": "total_cbd", "TOTAL CBD": "total_cbd",
        "Total Cannabinoids": "total_cannabinoids", "TOTAL CANNABINOIDS": "total_cannabinoids",
        "D8-THC": None, "DELTA-8-THC": None, "CBDV": None,
    }
    for aname, key in table_analytes.items():
        m = re.search(
            rf"(?im)^\s*{re.escape(aname)}\s+"
            rf"(?:[0-9,]*(?:\.[0-9]+)?\s+)?"
            rf"(ND|<LOQ|<LOD|<\s*LOQ|<\s*[0-9.]+|[0-9]*\.?[0-9]+)\s+"
            rf"(ND|<LOQ|<LOD|<\s*LOQ|<\s*[0-9.]+|[0-9]*\.?[0-9]+)?",
            text,
        )
        if not m:
            continue
        kind, val = parse_numeric_token(m.group(1))
        alt = {}
        if m.lastindex and m.lastindex >= 2 and m.group(2):
            k2, v2 = parse_numeric_token(m.group(2))
            if k2 == "numeric" and v2 is not None and kind == "numeric" and val is not None:
                # ChemHistory: mg/g then %; ACT: % then mg/g
                if v2 < val and v2 <= 100:
                    val, alt = v2, {"mg/g": val}
                    out["multi_unit"] = True
                else:
                    alt = {"mg/g": v2}
                    out["multi_unit"] = True
        if key is None:
            if kind == "nd":
                out["nd_cannabinoids"].append(aname)
            elif kind == "below_limit":
                out["below_limit_cannabinoids"].append(aname)
        else:
            _set_cann(out, key, kind, val, "%", alt or None)

    # Terpenes
    for m in re.finditer(
        r"(?i)\b(beta-caryophyllene|β-caryophyllene|limonene|d-limonene|linalool|myrcene|"
        r"beta-myrcene|alpha-humulene|humulene|alpha-pinene|beta-pinene|terpinolene|"
        r"ocimene|guaiol|bisabolol|nerolidol|camphene|valencene|geraniol|fenchol)\b"
        r"\s+(?:PASS\s+)?([0-9]*\.?[0-9]+|<0\.\d+|ND)\s*%?",
        text,
    ):
        kind, val = parse_numeric_token(m.group(2))
        name = m.group(1).lower().replace("β", "beta").replace("α", "alpha")
        if kind == "numeric" and val is not None:
            if not any(t["name"] == name for t in out["terpenes"]):
                out["terpenes"].append({"name": name, "value": val, "unit": "%"})
        elif kind == "nd":
            out["nd_terpenes"].append(name)
        elif kind == "below_limit":
            out["below_limit_terpenes"].append(name)

    out["panels"] = extract_panel_status(text)
    m = re.search(r"(?i)Moisture\s+(?:Pass(?:ed)?|Fail(?:ed)?)?.*?([0-9]*\.?[0-9]+)\s*%", text)
    if m:
        try:
            out["moisture"] = float(m.group(1))
        except ValueError:
            pass
    m = re.search(r"(?i)Water Activity.*?([0-1]\.[0-9]+)", text)
    if m:
        try:
            out["water_activity"] = float(m.group(1))
        except ValueError:
            pass
    if re.search(r"(?i)Foreign\s+(?:Matter|Material)[s]?\s+Pass", text):
        out["foreign_material"] = "pass"
    units_hit = len(re.findall(r"(?i)mg/g", text)) >= 2 and bool(re.search(r"%", text))
    if units_hit and out["cannabinoids"]:
        out["multi_unit"] = True
    if re.search(r"(?i)mg/(unit|serving)", text) and out["cannabinoids"]:
        out["multi_unit"] = True
    return out


def parse_source(url: str, text: str, html: str | None = None) -> dict[str, Any]:
    if "lims.tagleaf.com" in url or "tagleaf.com" in url:
        return parse_tagleaf(text)
    if "opencoa.org" in url:
        return parse_opencoa(html, text)
    return parse_generic(text)
