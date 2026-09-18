#!/usr/bin/env python3
"""WeedDAO Public COA Corpus v0.1 builder. Frozen schema. No fabricated numbers."""
from __future__ import annotations
import csv, hashlib, json, re, subprocess, sys, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

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
TRACKER = ROOT / "review-tracker.json"
EXPECTED_SHA = "31b0bdab4585954bebb9af1b06ac8b2d5a7b513ad1ca9694070836f1c723b5ee"
UA = "WeedDAOCorpusBot/0.1 (+research)"
TIMEOUT = 35
WORKERS = 5
CREATED_AT = "2026-09-18T17:00:00Z"
RETRIEVED_AT = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
CANN_KEYS = {"thc","thca","cbd","cbda","cbg","cbga","cbc","cbn","thcv","total_thc","total_cbd","total_cannabinoids"}
JMAP = {"new mexico":"US-NM","texas":"US-TX","missouri":"US-MO","new york":"US-NY","connecticut":"US-CT","massachusetts":"US-MA","louisiana brand / california lab":"US-CA","louisiana brand":"US-LA","texas retail / oregon laboratory":"US-OR"}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def jcode(hint: str | None) -> str | None:
    if not hint: return None
    h = hint.strip().lower()
    if h in JMAP: return JMAP[h]
    for k,v in JMAP.items():
        if k in h: return v
    return None

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

def parse_token(tok: str) -> tuple[str, float | None]:
    t = tok.strip().replace(",", "").replace("\xa0", " ")
    tl = t.lower()
    if tl in ("nd","n.d.","not detected","not_detected"): return "nd", None
    if tl in ("nt","not tested","not_tested","not performed","not_performed","n/t"): return "not_tested", None
    if tl in ("nr","not reported","not_reported","n/r"): return "not_reported", None
    if re.match(r"^<\s*(loq|lod|lor|rl)\b", tl) or tl.startswith("<loq") or tl.startswith("<lod"): return "below_limit", None
    if re.match(r"^<\s*[0-9]", t): return "below_limit", None
    m = re.match(r"^([0-9]*\.?[0-9]+)\s*$", t)
    if m: return "numeric", float(m.group(1))
    return "unknown", None

def cann_key(name: str) -> str | None:
    n = name.lower().strip()
    n = n.replace("−","-").replace("–","-").replace("δ","delta").replace("Δ","delta").replace("∆","delta")
    n = re.sub(r"&delta;?", "delta", n, flags=re.I)
    n = re.sub(r"\s+", " ", n)
    n = re.sub(r"delta\s*-?\s*9\s*-?\s*thc", "thc", n)
    n = re.sub(r"d\s*9\s*-?\s*thc", "thc", n)
    n = n.replace("thc-a","thca").replace("cbd-a","cbda").replace("cbg-a","cbga")
    n = n.replace("total thc","total_thc").replace("total cbd","total_cbd")
    n = n.replace("total cannabinoids","total_cannabinoids").replace("sum of cannabinoids","total_cannabinoids")
    n = n.replace(" ","_").replace("-","")
    aliases = {"thc":"thc","d9thc":"thc","delta9thc":"thc","thca":"thca","cbd":"cbd","cbda":"cbda","cbg":"cbg","cbga":"cbga","cbc":"cbc","cbn":"cbn","thcv":"thcv","total_thc":"total_thc","totalthc":"total_thc","total_cbd":"total_cbd","totalcbd":"total_cbd","total_cannabinoids":"total_cannabinoids","totalcannabinoids":"total_cannabinoids"}
    return aliases.get(n)

def empty_parsed() -> dict[str, Any]:
    return {"cannabinoids":{}, "terpenes":[], "nd_cannabinoids":[], "below_limit_cannabinoids":[], "nd_terpenes":[], "below_limit_terpenes":[], "multi_unit":False, "meta":{}, "panels":{"microbials":None,"pesticides":None,"heavy_metals":None,"residual_solvents":None,"mycotoxins":None}, "moisture":None, "water_activity":None, "foreign_material":None}

def panel_status(text: str) -> dict[str, str | None]:
    panels = {k: None for k in ("microbials","pesticides","heavy_metals","residual_solvents","mycotoxins")}
    def norm(s: str) -> str:
        s = s.lower().replace(" ","_")
        if s.startswith("pass"): return "pass"
        if s.startswith("fail"): return "fail"
        if "not_tested" in s or "not_performed" in s: return "not_tested"
        return s
    pats = [
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
    ]
    for pat, key in pats:
        m = re.search(pat, text)
        if m and panels[key] is None:
            panels[key] = norm(m.group(1))
    return panels

def set_cann(out, key, kind, value, unit="%", alt=None):
    if not key: return
    if kind == "numeric" and value is not None:
        if key in out["cannabinoids"] and out["cannabinoids"][key].get("kind")=="numeric": return
        out["cannabinoids"][key] = {"kind":"numeric","value":value,"unit":unit,"alt":alt or {}}
        if alt: out["multi_unit"] = True
    elif kind == "nd":
        if key not in out["nd_cannabinoids"]: out["nd_cannabinoids"].append(key)
    elif kind == "below_limit":
        if key not in out["below_limit_cannabinoids"]: out["below_limit_cannabinoids"].append(key)

def unit_schema(unit: str) -> str | None:
    u = (unit or "%").strip().lower()
    if u in ("%","percent"): return "%"
    if u == "mg/g": return "mg/g"
    if u in ("mg/ml",): return "mg/ml"
    if u in ("mg/serving","mg/unit","mg/srv"): return "mg/serving"
    return None

def mk_gap(key, semantics, severity, issue=None):
    return {"gap_key": key, "observed_source_semantics": semantics, "severity": severity, "existing_issue_if_any": issue}

def validate_record(path: Path) -> bool:
    return subprocess.run([str(PYTHON), str(VALIDATE), str(path)], capture_output=True, text=True).returncode == 0


def fetch_url(case_id: str, url: str) -> dict[str, Any]:
    result = {"case_id": case_id, "url": url, "ok": False, "status": None, "kind": "unknown", "text": "", "html": None, "error": None}
    if case_id in ("COA-001","COA-002","COA-003"):
        result.update({"ok": True, "kind": "seed", "status": 200}); return result
    CACHE.mkdir(parents=True, exist_ok=True)
    host = urlparse(url).netloc.replace(":","_")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{case_id}_{host}")[:100]
    raw_path = CACHE / f"{safe}.bin"; txt_path = CACHE / f"{safe}.txt"
    cookie = ["-b", "age_verified=1"] if "opencoa.org" in url else []
    cmd = ["curl","-sL","-A",UA,"--max-time",str(TIMEOUT),"-o",str(raw_path),"-w","%{http_code}",*cookie,url]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT+15)
        status = int((proc.stdout or "0").strip() or "0"); result["status"] = status
        if status != 200 or not raw_path.exists() or raw_path.stat().st_size < 100:
            result["error"] = f"HTTP {status} or empty"; return result
        magic = raw_path.read_bytes()[:5]
        is_pdf = magic.startswith(b"%PDF") or url.lower().endswith(".pdf") or ".pdf?" in url.lower()
        if is_pdf:
            result["kind"] = "pdf"
            pdf_path = CACHE / f"{safe}.pdf"; raw_path.replace(pdf_path)
            subprocess.run(["pdftotext","-layout",str(pdf_path),str(txt_path)], capture_output=True, timeout=60)
            try: pdf_path.unlink(missing_ok=True)
            except Exception: pass
            if txt_path.exists(): result["text"] = txt_path.read_text(encoding="utf-8", errors="ignore")
        else:
            result["kind"] = "html"
            html = raw_path.read_text(encoding="utf-8", errors="ignore"); result["html"] = html
            text = html_to_text(html); txt_path.write_text(text, encoding="utf-8"); result["text"] = text
            (CACHE / f"{safe}.html").write_text(html, encoding="utf-8")
            try: raw_path.unlink(missing_ok=True)
            except Exception: pass
        result["ok"] = bool((result.get("text") or "").strip())
        if not result["ok"]: result["error"] = "empty text"
        return result
    except Exception as e:
        result["error"] = str(e); return result

def parse_tagleaf(text: str) -> dict[str, Any]:
    out = empty_parsed(); t = text.replace("&Delta;","Δ").replace("&delta;","δ")
    for pat,key in [(r"Batch No\.\s*:\s*(\S+)","batch"),(r"Sample ID\s*:\s*(\S+)","sample"),(r"Batch Result\s*:\s*(\w+)","overall"),(r"METRC Src Tag\s*:\s*(\S+)","metrc_src"),(r"Metrc Testing Tag\s*:\s*(\S+)","metrc_test"),(r"Client\s*:\s*([^\n/]+)","client")]:
        m=re.search(pat,t)
        if m: out["meta"][key]=m.group(1).strip()
    analytes=[("Total THC","total_thc"),("Total CBD","total_cbd"),("Total Cannabinoids","total_cannabinoids"),("THCA","thca"),("CBGA","cbga"),("CBG","cbg"),("CBDA","cbda"),("CBD","cbd"),("CBC","cbc"),("CBN","cbn"),("THCV","thcv"),("Δ 9 -THC","thc"),("Δ9-THC","thc"),("Δ 8 -THC",None),("Δ8-THC",None),("CBCA",None),("CBDV",None),("THCVA",None),("CBDVA",None)]
    for aname,key in analytes:
        for m in re.finditer(re.escape(aname)+r"\s+([^\n]{0,60})", t, re.I):
            if re.search(r"(?i)per\s+(serving|package)", m.group(0)): continue
            rest=m.group(1).strip()
            mm=re.match(r"(ND|<LOQ|<LOD|<\s*LOQ|<\s*LOD|<\s*[0-9.]+|[0-9]*\.?[0-9]+)\s*%?\s*(ND|<LOQ|<LOD|<\s*LOQ|<\s*LOD|<\s*[0-9.]+|[0-9]*\.?[0-9]+)?", rest, re.I)
            if not mm: continue
            ka,va=parse_token(mm.group(1)); alt={}
            if mm.group(2):
                kb,vb=parse_token(mm.group(2))
                if kb=="numeric" and vb is not None: alt["mg/g"]=vb
            if key is None:
                if ka=="nd": out["nd_cannabinoids"].append(aname)
                elif ka=="below_limit": out["below_limit_cannabinoids"].append(aname)
            else:
                set_cann(out,key,ka,va,"%",alt or None)
            break
    mterp=re.search(r"Terpenes Testing.*?(?=Heavy Metals|Pesticide|Microbial|Foreign|Residual|Mycotoxin|Results Certified|$)", t, re.I|re.S)
    terp_sec=mterp.group(0) if mterp else t
    m=re.search(r"Total Terpenes\s+([0-9]*\.?[0-9]+)\s*%", terp_sec, re.I)
    if m: out["meta"]["total_terpenes"]=float(m.group(1))
    for tname in ["β -Caryophyllene","beta-Caryophyllene","d-Limonene","Limonene","Linalool","Nerolidol","β -Myrcene","beta-Myrcene","Myrcene","α -Bisabolol","alpha-Bisabolol","α -Humulene","alpha-Humulene","Humulene","Guaiol","β -Pinene","beta-Pinene","α -Pinene","alpha-Pinene","Camphene","Terpinolene","Ocimene","Geraniol","Eucalyptol"]:
        m=re.search(re.escape(tname)+r"\s+(ND|<LOQ|<LOD|<\s*LOQ|[0-9]*\.?[0-9]+)", terp_sec, re.I)
        if not m: continue
        kind,val=parse_token(m.group(1))
        display=tname.replace("β -","beta-").replace("α -","alpha-").replace("β-","beta-").replace("α-","alpha-")
        display=re.sub(r"\s+"," ",display).strip().lower()
        if kind=="numeric" and val is not None:
            if not any(x["name"]==display for x in out["terpenes"]): out["terpenes"].append({"name":display,"value":val,"unit":"%"})
        elif kind=="nd": out["nd_terpenes"].append(display)
        elif kind=="below_limit": out["below_limit_terpenes"].append(display)
    out["panels"]=panel_status(t)
    for key,pat in [("microbials",r"(?i)\bMicrobial\s+(Pass|Fail)\b"),("pesticides",r"(?i)\bPesticides?\s+(Pass|Fail)\b"),("heavy_metals",r"(?i)\bHeavy\s+Metals?\s+(Pass|Fail)\b"),("residual_solvents",r"(?i)\bResidual\s+Solvents?\s+(Pass|Fail)\b"),("mycotoxins",r"(?i)\bMycotoxins?\s+(Pass|Fail)\b")]:
        m=re.search(pat,t)
        if m and not out["panels"].get(key): out["panels"][key]=m.group(1).lower()
    if re.search(r"(?i)Foreign\s+Materials?\s+Pass", t): out["foreign_material"]="pass"
    if any(v.get("alt") for v in out["cannabinoids"].values()): out["multi_unit"]=True
    return out


def parse_generic(text: str) -> dict[str, Any]:
    out = empty_parsed()
    for pat, key in [(r"(?i)Batch\s*(?:Number|No\.?|#)?\s*[:#]?\s*([A-Za-z0-9][A-Za-z0-9._\-/]{1,40})","batch"),(r"(?i)Batch#:\s*([A-Za-z0-9._\-/]+)","batch"),(r"(?i)Sample(?:\s*ID)?\s*[:#]?\s*([A-Za-z0-9][A-Za-z0-9._\-/]{1,40})","sample"),(r"(?i)Lab ID:\s*(\S+)","sample"),(r"(?i)Strain:\s*([^\n]{2,60})","strain")]:
        m=re.search(pat,text)
        if m and key not in out["meta"]: out["meta"][key]=m.group(1).strip()
    for label,key in [("Total THC","total_thc"),("Total CBD","total_cbd"),("Total Cannabinoids","total_cannabinoids"),("Sum of Cannabinoids","total_cannabinoids")]:
        m=re.search(rf"(?i){re.escape(label)}\s*[:\s]+([0-9]*\.?[0-9]+)\s*(%|mg/g|mg/mL|mg/ml|mg/serving|mg/unit)?", text)
        if m and key not in out["cannabinoids"]:
            raw_u=(m.group(2) or "%"); rl=raw_u.lower(); unit="%"
            if "serving" in rl or "unit" in rl: unit="mg/serving"
            elif "ml" in rl: unit="mg/ml"
            elif rl=="mg/g": unit="mg/g"
            set_cann(out,key,"numeric",float(m.group(1)),unit)
    table={"THCa":"thca","THCA":"thca","D9-THC":"thc","Δ9-THC":"thc","d9-THC":"thc","DELTA-9-THC":"thc","DELTA-9 THC":"thc","CBD":"cbd","CBDa":"cbda","CBDA":"cbda","CBG":"cbg","CBGa":"cbga","CBGA":"cbga","CBC":"cbc","CBN":"cbn","THCV":"thcv","Total THC":"total_thc","TOTAL THC":"total_thc","Total CBD":"total_cbd","TOTAL CBD":"total_cbd","Total Cannabinoids":"total_cannabinoids","TOTAL CANNABINOIDS":"total_cannabinoids","D8-THC":None,"DELTA-8-THC":None,"CBDV":None}
    for aname,key in table.items():
        m=re.search(rf"(?im)^\s*{re.escape(aname)}\s+(?:[0-9,]*(?:\.[0-9]+)?\s+)?(ND|<LOQ|<LOD|<\s*LOQ|<\s*[0-9.]+|[0-9]*\.?[0-9]+)\s+(ND|<LOQ|<LOD|<\s*LOQ|<\s*[0-9.]+|[0-9]*\.?[0-9]+)?", text)
        if not m: continue
        kind,val=parse_token(m.group(1)); alt={}
        if m.lastindex and m.lastindex>=2 and m.group(2):
            k2,v2=parse_token(m.group(2))
            if k2=="numeric" and v2 is not None and kind=="numeric" and val is not None:
                if v2<val and v2<=100: val,alt=v2,{"mg/g":val}; out["multi_unit"]=True
                else: alt={"mg/g":v2}; out["multi_unit"]=True
        if key is None:
            if kind=="nd": out["nd_cannabinoids"].append(aname)
            elif kind=="below_limit": out["below_limit_cannabinoids"].append(aname)
        else:
            set_cann(out,key,kind,val,"%",alt or None)
    for m in re.finditer(r"(?i)\b(beta-caryophyllene|β-caryophyllene|limonene|d-limonene|linalool|myrcene|beta-myrcene|alpha-humulene|humulene|alpha-pinene|beta-pinene|terpinolene|ocimene|guaiol|bisabolol|nerolidol|camphene|valencene|geraniol|fenchol)\b\s+(?:PASS\s+)?([0-9]*\.?[0-9]+|<0\.\d+|ND)\s*%?", text):
        kind,val=parse_token(m.group(2)); name=m.group(1).lower().replace("β","beta").replace("α","alpha")
        if kind=="numeric" and val is not None:
            if not any(t["name"]==name for t in out["terpenes"]): out["terpenes"].append({"name":name,"value":val,"unit":"%"})
        elif kind=="nd": out["nd_terpenes"].append(name)
        elif kind=="below_limit": out["below_limit_terpenes"].append(name)
    out["panels"]=panel_status(text)
    m=re.search(r"(?i)Moisture\s+(?:Pass(?:ed)?|Fail(?:ed)?)?.*?([0-9]*\.?[0-9]+)\s*%", text)
    if m:
        try: out["moisture"]=float(m.group(1))
        except ValueError: pass
    m=re.search(r"(?i)Water Activity.*?([0-1]\.[0-9]+)", text)
    if m:
        try: out["water_activity"]=float(m.group(1))
        except ValueError: pass
    if re.search(r"(?i)Foreign\s+(?:Matter|Material)[s]?\s+Pass", text): out["foreign_material"]="pass"
    if len(re.findall(r"(?i)mg/g", text))>=2 and re.search(r"%", text) and out["cannabinoids"]: out["multi_unit"]=True
    if re.search(r"(?i)mg/(unit|serving)", text) and out["cannabinoids"]: out["multi_unit"]=True
    return out

def parse_opencoa(html: str | None, text: str) -> dict[str, Any]:
    out = parse_generic(text); src = html or text
    for m in re.finditer(r"(?is)(Δ9-THC|THC-A|THCA|CBD|CBG|CBDA|Total\s*THC|Total\s*CBD)\s*</span>\s*<span[^>]*>\s*([0-9]*\.?[0-9]+)\s*%", src):
        set_cann(out, cann_key(m.group(1).replace("THC-A","THCA")), "numeric", float(m.group(2)), "%")
    for m in re.finditer(r"(?i)(Δ9-THC|THCA|CBD|CBG|Total\s*THC|Total\s*CBD)\s+([0-9]*\.?[0-9]+)\s*%", text):
        set_cann(out, cann_key(m.group(1)), "numeric", float(m.group(2)), "%")
    for key,pat in [("microbials",r"(?i)microbials?\s*\([^)]*\)[\s\S]{0,80}?Pass"),("pesticides",r"(?i)pesticides?\s*\([^)]*\)[\s\S]{0,80}?Pass"),("heavy_metals",r"(?i)heavy metals?[\s\S]{0,120}?Pass"),("residual_solvents",r"(?i)residual solvents?\s*\([^)]*\)[\s\S]{0,80}?Pass"),("mycotoxins",r"(?i)mycotoxins?\s*\([^)]*\)[\s\S]{0,80}?Pass")]:
        if out["panels"].get(key) is None and re.search(pat, text): out["panels"][key]="pass"
    return out

def parse_source(url: str, text: str, html: str | None = None) -> dict[str, Any]:
    if "tagleaf.com" in url: return parse_tagleaf(text)
    if "opencoa.org" in url: return parse_opencoa(html, text)
    return parse_generic(text)


SEED_GAPS = {
  "COA-001": [
    mk_gap("below_reporting_limit_qualifier","Cannabinoid/terpene <LOQ","CRITICAL_INTEROPERABILITY",1),
    mk_gap("analyte_level_not_performed","Not Performed analytes","CRITICAL_INTEROPERABILITY",2),
    mk_gap("extended_cannabinoid_vocabulary","Δ8/Δ10/THCP/CBDV","IMPORTANT"),
    mk_gap("sample_lifecycle_metadata","Received/collected metadata","IMPORTANT"),
    mk_gap("foreign_material","Passed Visual Inspection","IMPORTANT"),
    mk_gap("multi_unit_cannabinoid","mg/g + %","CRITICAL_INTEROPERABILITY",4),
    mk_gap("moisture_not_in_core","Moisture Not Performed","OPTIONAL"),
  ],
  "COA-002": [
    mk_gap("nd_not_representable","Cannabinoid/terpene ND","CRITICAL_INTEROPERABILITY",3),
    mk_gap("below_reporting_limit_qualifier","Heavy metals <0.008 ppm","CRITICAL_INTEROPERABILITY",1),
    mk_gap("multi_unit_cannabinoid","%wt + mg/g + mg/unit","CRITICAL_INTEROPERABILITY",4),
    mk_gap("foreign_material","Visual Inspection Passed","IMPORTANT"),
    mk_gap("best_by_date","Best by on COA","OPTIONAL"),
  ],
  "COA-003": [
    mk_gap("nd_not_representable","Cannabinoid/terpene ND","CRITICAL_INTEROPERABILITY",3),
    mk_gap("below_reporting_limit_qualifier","Heavy metals <0.008 ppm","CRITICAL_INTEROPERABILITY",1),
    mk_gap("multi_unit_cannabinoid","%wt + mg/g + mg/unit","CRITICAL_INTEROPERABILITY",4),
    mk_gap("literal_batch_id_zero","Batch ID literal 0","IMPORTANT"),
    mk_gap("foreign_material","Visual Inspection Passed","IMPORTANT"),
  ],
}

def map_seed(case_id: str, meta: dict) -> tuple[dict, dict, dict]:
    n = case_id.split("-")[1]
    record = json.loads((REVIEW_DATA / f"coa-{n}-weeddao-record.json").read_text())
    source = {
        "case_id": case_id, "source_url": meta["source_url"], "source_tier": meta["source_tier"],
        "source_group": meta.get("source_group"), "jurisdiction_hint": meta.get("jurisdiction_hint"),
        "product_hint": meta.get("product_hint"), "product_type_hint": meta.get("product_type_hint"),
        "seed_reuse": True,
        "laboratory": {"COA-001":"external-lab-001","COA-002":"external-lab-002","COA-003":"external-lab-002"}[case_id],
        "producer_or_brand": record["producer"]["organization_name"],
        "batch_or_lot_id": record.get("cultivation_batch_id"),
        "sample_id": (record.get("lab_results") or {}).get("sample_id"),
        "detail_level": "high",
        "notes": "Seed case: reused hand-reviewed WeedDAO mapping; original COA image not republished.",
    }
    gaps = SEED_GAPS[case_id]
    review = {
        "case_id": case_id, "schema_version": "0.1-alpha", "mapped_record_valid": True,
        "mapping_result": "PARTIAL",
        "exact_mapping_count": {"COA-001":12,"COA-002":14,"COA-003":13}[case_id],
        "partial_mapping_count": {"COA-001":6,"COA-002":5,"COA-003":5}[case_id],
        "not_representable_count": len(gaps), "gaps": gaps, "source_unavailable": False,
        "notes": "Seed hand-reviewed PARTIAL mapping; confirms issues #1-#4 as applicable.",
    }
    return source, record, review

def map_new(case_id: str, meta: dict, ext: dict, parsed: dict | None, fetch_ok: bool) -> tuple[dict, dict]:
    gaps=[]; exact=0; partial=0
    parsed = parsed or empty_parsed()
    batch = ext.get("batch_observed") or parsed.get("meta",{}).get("batch")
    sample = ext.get("sample_observed") or parsed.get("meta",{}).get("sample")
    if batch is not None and str(batch) != "":
        cultivation_batch_id = str(batch); exact += 1
    elif sample:
        cultivation_batch_id = str(sample); partial += 1
        gaps.append(mk_gap("batch_id_missing_used_sample","No batch id; used sample id","IMPORTANT"))
    else:
        cultivation_batch_id = f"corpus-{case_id.lower()}-unknown-batch"; partial += 1
        gaps.append(mk_gap("batch_id_missing_placeholder","No batch/sample id; deterministic placeholder","IMPORTANT"))
    lab = ext.get("laboratory_verified_or_observed")
    client = ext.get("client_observed")
    product = meta.get("product_hint") or ext.get("title_verified")
    record = {
        "schema_version": "0.1-alpha",
        "record_id": f"corpus-{case_id.lower()}",
        "cultivation_batch_id": cultivation_batch_id,
        "created_at": CREATED_AT,
        "updated_at": CREATED_AT,
        "producer": {"organization_name": client or meta.get("source_group") or "unknown-producer", "jurisdiction": jcode(meta.get("jurisdiction_hint"))},
        "cultivar": {"reported_name": ((str(product).split("(")[0].strip()[:120] if product else "unknown") or "unknown"), "identity_status": "reported"},
        "lab_results": {
            "lab_name": lab, "sample_id": sample,
            "provenance": "laboratory_verified" if fetch_ok else "derived",
            "notes": f"Mapped from public COA corpus case {case_id}. WeedDAO does not independently re-verify laboratory measurements.",
        },
        "provenance": {
            "record": "derived",
            "lab_results": "laboratory_verified" if fetch_ok else "derived",
            "notes": "Public COA corpus mapping by WeedDAO Research. Not an external implementation claim.",
        },
        "extensions": {"weeddao_corpus": {
            "case_id": case_id, "source_url": meta["source_url"], "source_tier": meta["source_tier"],
            "source_group": meta.get("source_group"), "product_hint": meta.get("product_hint"),
            "product_type_hint": meta.get("product_type_hint"), "title_verified": ext.get("title_verified"),
            "overall_result_observed": ext.get("overall_result_observed"),
            "units_observed": ext.get("units_observed"), "panels_observed": ext.get("panels_observed"),
        }},
    }
    cann = {}
    for key, entry in (parsed.get("cannabinoids") or {}).items():
        if key not in CANN_KEYS: continue
        if entry.get("kind") != "numeric" or entry.get("value") is None: continue
        unit = unit_schema(entry.get("unit") or "%")
        if unit is None: continue
        cann[key] = {"value": entry["value"], "unit": unit, "provenance": "laboratory_verified"}
        exact += 1
        if entry.get("alt"):
            record["extensions"]["weeddao_corpus"].setdefault("cannabinoids_alt_units", {})[key] = entry["alt"]
            parsed["multi_unit"] = True
    if cann: record["lab_results"]["cannabinoids"] = cann
    terps = []
    for t in parsed.get("terpenes") or []:
        if t.get("value") is None: continue
        unit = t.get("unit") or "%"
        if unit not in ("%", "mg/g", "ppm"): unit = "%"
        terps.append({"name": t["name"], "value": t["value"], "unit": unit}); exact += 1
    if terps: record["lab_results"]["terpenes"] = terps
    if parsed.get("meta", {}).get("total_terpenes") is not None:
        record["lab_results"]["total_terpenes"] = {"value": parsed["meta"]["total_terpenes"], "unit": "%"}; exact += 1
    safety = {}
    for pkey in ("microbials","pesticides","heavy_metals","residual_solvents","mycotoxins"):
        st = (parsed.get("panels") or {}).get(pkey)
        if st in ("pass","fail","not_tested","partial","not_applicable"):
            safety[pkey] = {"status": st}; exact += 1
    if safety: record["lab_results"]["safety"] = safety

    if parsed.get("nd_cannabinoids") or parsed.get("nd_terpenes") or ext.get("uses_nd"):
        gaps.append(mk_gap("nd_not_representable", f"ND examples={list(parsed.get('nd_cannabinoids') or [])[:8]}", "CRITICAL_INTEROPERABILITY", 3))
    if parsed.get("below_limit_cannabinoids") or parsed.get("below_limit_terpenes") or ext.get("uses_below_limit"):
        gaps.append(mk_gap("below_reporting_limit_qualifier", f"Below-limit examples={list(parsed.get('below_limit_cannabinoids') or [])[:8]}", "CRITICAL_INTEROPERABILITY", 1))
    units = ext.get("units_observed") or []
    multi = bool(parsed.get("multi_unit")) or len([u for u in units if any(x in str(u).lower() for x in ("%","mg/g","mg/serving","mg/ml","mg/unit"))]) >= 2
    if multi:
        gaps.append(mk_gap("multi_unit_cannabinoid", f"units_observed={units}", "CRITICAL_INTEROPERABILITY", 4))
    if ext.get("uses_not_performed") or ext.get("uses_nt_or_not_tested"):
        gaps.append(mk_gap("analyte_level_not_performed", "NOT TESTED / NOT PERFORMED", "CRITICAL_INTEROPERABILITY", 2))
    if ext.get("uses_nr_or_not_reported"):
        gaps.append(mk_gap("not_reported", "NOT REPORTED", "IMPORTANT"))
    if ext.get("has_metrc_or_regulatory_tracking") or parsed.get("meta",{}).get("metrc_src"):
        gaps.append(mk_gap("regulatory_tracking", "METRC/regulatory tracking", "JURISDICTION_SPECIFIC")); partial += 1
        if parsed.get("meta",{}).get("metrc_src"): record["extensions"]["weeddao_corpus"]["metrc_src_tag"] = parsed["meta"]["metrc_src"]
        if parsed.get("meta",{}).get("metrc_test"): record["extensions"]["weeddao_corpus"]["metrc_testing_tag"] = parsed["meta"]["metrc_test"]
    if ext.get("has_sample_lifecycle_metadata"):
        gaps.append(mk_gap("sample_lifecycle_metadata", "Collected/received lifecycle metadata", "IMPORTANT"))
    panels_obs = set(ext.get("panels_observed") or [])
    if "foreign_matter" in panels_obs or parsed.get("foreign_material"):
        gaps.append(mk_gap("foreign_material", "Foreign material / visual inspection", "IMPORTANT")); partial += 1
        record["extensions"]["weeddao_corpus"]["foreign_material"] = parsed.get("foreign_material") or "observed"
    if "moisture" in panels_obs or parsed.get("moisture") is not None:
        gaps.append(mk_gap("moisture_not_in_core", "Moisture on source", "OPTIONAL")); partial += 1
        if parsed.get("moisture") is not None: record["extensions"]["weeddao_corpus"]["moisture_percent"] = parsed["moisture"]
    if "water_activity" in panels_obs or parsed.get("water_activity") is not None:
        gaps.append(mk_gap("water_activity_not_in_core", "Water activity on source", "OPTIONAL")); partial += 1
        if parsed.get("water_activity") is not None: record["extensions"]["weeddao_corpus"]["water_activity"] = parsed["water_activity"]
    if not fetch_ok:
        gaps.append(mk_gap("source_unavailable_or_unparsed", "SOURCE_UNAVAILABLE at fetch time", "IMPORTANT"))
        record["extensions"]["weeddao_corpus"]["source_unavailable"] = True
        record["lab_results"]["notes"] += " SOURCE_UNAVAILABLE at corpus fetch time."
    if not cann and not terps and fetch_ok:
        gaps.append(mk_gap("analyte_tables_unparsed", "Fetch ok but analyte tables not reliably parsed", "IMPORTANT"))

    important = {"nd_not_representable","below_reporting_limit_qualifier","multi_unit_cannabinoid","analyte_level_not_performed","source_unavailable_or_unparsed"}
    dropped = any(g["gap_key"] in important for g in gaps)
    has_numeric = bool(cann) or bool(terps)
    if dropped: mapping_result = "PARTIAL"
    elif has_numeric and not gaps: mapping_result = "FULL"
    elif has_numeric and all(g["severity"] in ("OPTIONAL","JURISDICTION_SPECIFIC","NICE_TO_HAVE") for g in gaps): mapping_result = "FULL"
    else: mapping_result = "PARTIAL"
    if dropped: mapping_result = "PARTIAL"

    review = {
        "case_id": case_id, "schema_version": "0.1-alpha", "mapped_record_valid": False,
        "mapping_result": mapping_result, "exact_mapping_count": exact, "partial_mapping_count": partial,
        "not_representable_count": len(gaps), "gaps": gaps, "source_unavailable": not fetch_ok,
        "notes": "Automated corpus mapping against frozen v0.1-alpha; numeric values only when parseable; no fabrication.",
    }
    return record, review


def build_source(case_id, meta, ext, fetch):
    return {
        "case_id": case_id, "source_url": meta["source_url"], "source_tier": meta["source_tier"],
        "source_group": meta.get("source_group"), "retrieved_at": RETRIEVED_AT,
        "fetch_status": (fetch or {}).get("status"), "fetch_ok": bool(fetch and fetch.get("ok")),
        "source_unavailable": bool(fetch is not None and not fetch.get("ok")),
        "jurisdiction_hint": meta.get("jurisdiction_hint"),
        "producer_or_brand": ext.get("client_observed") or meta.get("source_group"),
        "laboratory": ext.get("laboratory_verified_or_observed"),
        "product_name": meta.get("product_hint") or ext.get("title_verified"),
        "product_type": meta.get("product_type_hint"),
        "batch_or_lot_id": ext.get("batch_observed"), "sample_id": ext.get("sample_observed"),
        "overall_status": ext.get("overall_result_observed"), "title_verified": ext.get("title_verified"),
        "panels_observed": ext.get("panels_observed"), "units_observed": ext.get("units_observed"),
        "uses_nd": ext.get("uses_nd"), "uses_below_limit": ext.get("uses_below_limit"),
        "uses_not_tested": ext.get("uses_nt_or_not_tested"), "uses_not_reported": ext.get("uses_nr_or_not_reported"),
        "uses_not_performed": ext.get("uses_not_performed"),
        "has_regulatory_tracking": ext.get("has_metrc_or_regulatory_tracking"),
        "has_sample_lifecycle": ext.get("has_sample_lifecycle_metadata"),
        "detail_level": meta.get("detail_level") or ext.get("detail_level"),
        "verification_method": meta.get("verification_method"), "notes": ext.get("mapping_note"),
    }

def panel_flags(ext):
    panels = set(ext.get("panels_observed") or [])
    def has(name):
        return (name in panels) if panels else None
    return {
        "has_cannabinoids": has("cannabinoid"), "has_terpenes": has("terpene"),
        "has_microbials": has("microbial"), "has_pesticides": has("pesticide"),
        "has_heavy_metals": has("heavy_metal"), "has_residual_solvents": has("residual_solvent"),
        "has_mycotoxins": has("mycotoxin"), "has_moisture": has("moisture"),
        "has_water_activity": has("water_activity"), "has_foreign_material": has("foreign_matter"),
    }

def compute_stats(manifest_rows, reviews):
    from collections import defaultdict
    primary = sum(1 for r in manifest_rows if r["source_tier"]=="primary")
    secondary = sum(1 for r in manifest_rows if r["source_tier"]=="secondary")
    seed = sum(1 for r in manifest_rows if str(r["source_tier"]).startswith("seed"))
    full = sum(1 for r in reviews if r["mapping_result"]=="FULL")
    partial = sum(1 for r in reviews if r["mapping_result"]=="PARTIAL")
    failed = sum(1 for r in reviews if r["mapping_result"]=="FAILED")
    unavail = sum(1 for r in manifest_rows if "SOURCE_UNAVAILABLE" in (r.get("notes") or ""))
    jurisdictions = sorted({r.get("jurisdiction") for r in manifest_rows if r.get("jurisdiction")})
    labs = sorted({r.get("laboratory") for r in manifest_rows if r.get("laboratory")})
    producers = sorted({r.get("producer_or_brand") for r in manifest_rows if r.get("producer_or_brand")})
    ptypes = sorted({r.get("product_type") for r in manifest_rows if r.get("product_type")})
    gap_cases=defaultdict(set); gap_labs=defaultdict(set); gap_jurs=defaultdict(set); gap_ptypes=defaultdict(set)
    gap_sev={}; gap_issue={}
    man_by={r["case_id"]: r for r in manifest_rows}
    for rev in reviews:
        m=man_by[rev["case_id"]]
        for g in rev.get("gaps") or []:
            k=g["gap_key"]; gap_cases[k].add(rev["case_id"])
            if m.get("laboratory"): gap_labs[k].add(m["laboratory"])
            if m.get("jurisdiction"): gap_jurs[k].add(m["jurisdiction"])
            if m.get("product_type"): gap_ptypes[k].add(m["product_type"])
            gap_sev[k]=g.get("severity") or gap_sev.get(k)
            if g.get("existing_issue_if_any") is not None: gap_issue[k]=g["existing_issue_if_any"]
    gap_stats=[]
    for k,cases in sorted(gap_cases.items(), key=lambda x: -len(x[1])):
        n=len(cases); labs_c=gap_labs[k]; jurs_c=gap_jurs[k]
        evidence="SINGLE_CASE"
        if n>=2: evidence="REPEATED"
        if len({man_by[c].get("producer_or_brand") for c in cases if man_by[c].get("producer_or_brand")})>1: evidence="CROSS_PRODUCER"
        if len(labs_c)>1: evidence="CROSS_LAB"
        if len(jurs_c)>1: evidence="CROSS_JURISDICTION"
        gap_stats.append({"gap_key":k,"cases_count":n,"cases_percent":round(100.0*n/50,1),"independent_labs_count":len(labs_c),"jurisdictions_count":len(jurs_c),"product_types_count":len(gap_ptypes[k]),"severity":gap_sev.get(k),"existing_issue":gap_issue.get(k),"evidence_class":evidence,"case_ids":sorted(cases)})
    occ={
        "ND": sum(1 for r in manifest_rows if r.get("uses_nd")),
        "below_limit": sum(1 for r in manifest_rows if r.get("uses_below_limit")),
        "NOT_TESTED_OR_NOT_PERFORMED": sum(1 for r in manifest_rows if r.get("uses_not_tested")),
        "NOT_REPORTED": sum(1 for r in manifest_rows if r.get("uses_not_reported")),
        "multi_unit": sum(1 for r in manifest_rows if r.get("uses_multi_unit")),
        "sample_lifecycle": sum(1 for r in manifest_rows if r.get("has_sample_lifecycle")),
        "regulatory_tracking": sum(1 for r in manifest_rows if r.get("has_regulatory_tracking")),
        "water_activity": sum(1 for r in manifest_rows if r.get("has_water_activity")),
        "moisture": sum(1 for r in manifest_rows if r.get("has_moisture")),
        "foreign_material": sum(1 for r in manifest_rows if r.get("has_foreign_material")),
        "FAIL": sum(1 for r in manifest_rows if r.get("contains_failure")),
    }
    return {"TOTAL_CASES":50,"SEED_CASES":seed,"NEW_PUBLIC_CASES":47,"PRIMARY_SOURCE_CASES":primary,"SECONDARY_SOURCE_CASES":secondary,"JURISDICTIONS":jurisdictions,"LABORATORIES":labs,"PRODUCERS":producers,"PRODUCT_TYPES":ptypes,"FULL_MAPPINGS":full,"PARTIAL_MAPPINGS":partial,"FAILED_MAPPINGS":failed,"SOURCE_UNAVAILABLE":unavail,"gap_stats":gap_stats,"occurrences":occ}

def write_docs(stats):
    (CORPUS/"README.md").write_text(f"""# WeedDAO Public COA Corpus v0.1

Public evidence collection mapping real-world Certificates of Analysis to frozen WeedDAO Cultivation Record **v0.1-alpha**.

**Not claims of** industry adoption, certification, lab endorsement, or `FIRST_EXTERNAL_IMPLEMENTATION`. WeedDAO Research mapped these public sources for schema-validation evidence.

## Freeze
- Schema `schemas/weeddao-cultivation-record-v0.1-alpha.schema.json` is **FROZEN**
- SHA256: `{EXPECTED_SHA}`
- Tag `v0.1-alpha` must not move
- ND / `<LOQ` / NOT TESTED are never coerced

## Layout
| Path | Description |
|------|-------------|
| `manifest.json` / `manifest.csv` | 50-case index |
| `cases/coa-NNN-source.json` | Source metadata |
| `mappings/coa-NNN-weeddao-record.json` | Mapped records |
| `reviews/coa-NNN-review.json` | Mapping result + gaps |
| `inputs/` | Verified manifest + extraction jsonl |
| `cache/` | Local fetch cache (gitignored) |

## Cases
- **COA-001..003** — hand-reviewed seed mappings
- **COA-004..050** — verified public sources (37 primary, 10 secondary OpenCOA)

## Validate
```bash
python scripts/validate.py
python scripts/validate.py corpus/v0.1/mappings/*.json
```

## Rebuild
```bash
/workspace/weeddao/.venv/bin/python corpus/v0.1/scripts/build_corpus.py
```

## Counts
- TOTAL={stats['TOTAL_CASES']} PRIMARY={stats['PRIMARY_SOURCE_CASES']} SECONDARY={stats['SECONDARY_SOURCE_CASES']}
- FULL/PARTIAL/FAILED={stats['FULL_MAPPINGS']}/{stats['PARTIAL_MAPPINGS']}/{stats['FAILED_MAPPINGS']}
""", encoding="utf-8")

    (DOCS/"corpus-v0.1-methodology.md").write_text(f"""# Corpus v0.1 Methodology

## Objective
Build a 50-case public COA corpus testing WeedDAO Cultivation Record **v0.1-alpha** interoperability without modifying the frozen schema.

## Authoritative inputs
1. `corpus/v0.1/inputs/weeddao_verified_manifest_v0.1.json` — official verified case list (`verified_total_cases=50`).
2. `corpus/v0.1/inputs/weeddao_extracted_coa_data_v0.1.jsonl` — interoperability metadata.
3. Seed mappings in `review-data/coa-00{{1,2,3}}-weeddao-record.json`.

`replacement_case_ids` in the verified manifest are historical (already applied); this build does not re-replace sources.

## Freeze rules
- Do not modify the v0.1-alpha schema
- Expected SHA256: `{EXPECTED_SHA}`
- Do not move git tag `v0.1-alpha`
- Do not design v0.2 schema here

## Fetch policy
- Fetch **only** the exact `source_url` from the verified manifest
- User-Agent: `{UA}`
- Timeout ~{TIMEOUT}s
- OpenCOA: cookie `age_verified=1`
- TagLeaf: HTML scrape
- PDF hosts: download → `pdftotext -layout` → parse; **do not commit PDF binaries**
- On failure: `SOURCE_UNAVAILABLE` and continue (no replacement search)

## Mapping rules
- Required: `schema_version`, `record_id`, `cultivation_batch_id`, `created_at`
- `cultivation_batch_id`: batch_observed OR sample_observed OR deterministic `corpus-coa-NNN-unknown-batch`
- Detected numeric cannabinoids → CannabinoidMeasurement with unit ∈ {{%, mg/g, mg/ml, mg/serving}}; prefer `%` when multi-unit; alts in `extensions.weeddao_corpus`
- ND cannabinoids/terpenes: **omit**; gap (issue #3)
- `<LOQ`/`<LOD`/`<n`: **omit**; gap (issue #1)
- Panel PASS/FAIL/NOT_TESTED → `lab_results.safety.*.status`
- Mycotoxins panel status is first-class; moisture / water activity / foreign material → extensions + gaps
- `mapping_result`: FULL only if no important semantics dropped; else PARTIAL; FAILED if no valid record

## Limitations
- Best-effort parsers; some PDFs are layout-noisy
- Seed labs remain redacted (`external-lab-00x`)
- Corpus is WeedDAO-authored mappings, not external software adoption

## Pipeline
`corpus/v0.1/scripts/build_corpus.py`
""", encoding="utf-8")

    lines=["# Corpus v0.1 Analysis\n","Evidence-only analysis against frozen v0.1-alpha.\n","## Summary counts\n"]
    for k in ["TOTAL_CASES","SEED_CASES","NEW_PUBLIC_CASES","PRIMARY_SOURCE_CASES","SECONDARY_SOURCE_CASES","FULL_MAPPINGS","PARTIAL_MAPPINGS","FAILED_MAPPINGS","SOURCE_UNAVAILABLE"]:
        lines.append(f"- **{k}** = {stats[k]}")
    lines += ["\n### Jurisdictions\n"] + [f"- {j}" for j in stats["JURISDICTIONS"]]
    lines += ["\n### Laboratories\n"] + [f"- {j}" for j in stats["LABORATORIES"]]
    lines += ["\n### Producers / brands / clients\n"] + [f"- {j}" for j in stats["PRODUCERS"]]
    lines += ["\n### Product types\n"] + [f"- {j}" for j in stats["PRODUCT_TYPES"]]
    lines.append("\n## Occurrence counts\n")
    for k,v in stats["occurrences"].items(): lines.append(f"- **{k}**: {v} / 50")
    lines.append("\n## Gap statistics\n")
    lines.append("| gap_key | cases | % | labs | jurisdictions | product_types | severity | existing_issue | evidence_class |")
    lines.append("|---------|------:|--:|-----:|--------------:|--------------:|----------|----------------|----------------|")
    for g in stats["gap_stats"]:
        lines.append(f"| `{g['gap_key']}` | {g['cases_count']} | {g['cases_percent']} | {g['independent_labs_count']} | {g['jurisdictions_count']} | {g['product_types_count']} | {g['severity']} | {g['existing_issue']} | {g['evidence_class']} |")
    lines.append("\n## Existing issues #1–#4 confirmation\n")
    issue_map={1:"below_reporting_limit_qualifier",2:"analyte_level_not_performed",3:"nd_not_representable",4:"multi_unit_cannabinoid"}
    for num,key in issue_map.items():
        g=next((x for x in stats["gap_stats"] if x["gap_key"]==key), None)
        if g: lines.append(f"- **Issue #{num}** (`{key}`): {g['cases_count']} cases ({g['cases_percent']}%), labs={g['independent_labs_count']}, jurisdictions={g['jurisdictions_count']}, evidence={g['evidence_class']}")
        else: lines.append(f"- **Issue #{num}** (`{key}`): no exact gap_key rows (check related keys)")
    lines += ["\n## FAIL / numeric contaminant PASS / missing panels\n", f"- Actual FAIL overall_status rows: {stats['occurrences']['FAIL']}", "- Numeric contaminant detections that still PASS: not systematically quantified; `<` analyte rows never coerced to 0.", "- Missing panels: omission or `not_tested` when source says NOT PERFORMED/NOT TESTED; never PASS.\n"]
    (DOCS/"corpus-v0.1-analysis.md").write_text("\n".join(lines)+"\n", encoding="utf-8")

    high,mod,low,juris,present=[],[],[],[],[]
    for g in stats["gap_stats"]:
        entry={"gap_key":g["gap_key"],"cases_count":g["cases_count"],"evidence_class":g["evidence_class"],"severity":g["severity"],"existing_issue":g["existing_issue"]}
        if g["existing_issue"] in (1,2,3,4) or (g["cases_count"]>=5 and g["evidence_class"] in ("CROSS_LAB","CROSS_JURISDICTION","CROSS_PRODUCER") and g["severity"]=="CRITICAL_INTEROPERABILITY"): high.append(entry)
        elif g["severity"]=="JURISDICTION_SPECIFIC": juris.append(entry)
        elif g["gap_key"] in ("foreign_material","moisture_not_in_core","water_activity_not_in_core","best_by_date"): present.append(entry)
        elif g["cases_count"]>=3 and g["severity"] in ("CRITICAL_INTEROPERABILITY","IMPORTANT"): mod.append(entry)
        else: low.append(entry)
    er=["# v0.2 Evidence Readiness (no schema design)\n","Evidence strength only. **No v0.2 schema proposed here.**\n","## HIGH_CONFIDENCE_RECURRING_GAPS\n"]
    er += [f"- `{e['gap_key']}` — {e['cases_count']} cases, {e['evidence_class']}, severity={e['severity']}, existing_issue={e['existing_issue']}" for e in high]
    er += ["\n## MODERATE_EVIDENCE_GAPS\n"] + [f"- `{e['gap_key']}` — {e['cases_count']} cases, {e['evidence_class']}" for e in mod]
    er += ["\n## LOW_EVIDENCE_GAPS\n"] + [f"- `{e['gap_key']}` — {e['cases_count']} cases" for e in low]
    er += ["\n## JURISDICTION_SPECIFIC_FIELDS\n"] + [f"- `{e['gap_key']}` — {e['cases_count']} cases" for e in juris]
    er += ["\n## PRESENTATION_ONLY_FIELDS\n"] + [f"- `{e['gap_key']}` — {e['cases_count']} cases" for e in present]
    er += ["\n## Explicit non-actions\n","- No v0.2 schema authored here.","- Issues #1–#4 confirmed with corpus counts; do not duplicate.","- New GitHub issues only if a new CRITICAL_INTEROPERABILITY gap appears in ≥2 independent COAs (preferably >1 lab/producer) or one severe safety/dosing/traceability failure.\n"]
    (DOCS/"v0.2-evidence-readiness.md").write_text("\n".join(er)+"\n", encoding="utf-8")
    write_json(CORPUS/"build_stats.json", stats)

def update_tracker(stats):
    data=json.loads(TRACKER.read_text())
    data["updated_at"]="2026-09-18"
    data["PUBLIC_COA_CORPUS_V0_1"]={
        "status":"COMPLETED","path":"corpus/v0.1/","manifest":"corpus/v0.1/manifest.json",
        "analysis":"docs/corpus-v0.1-analysis.md","methodology":"docs/corpus-v0.1-methodology.md",
        "evidence_readiness":"docs/v0.2-evidence-readiness.md","total_cases":50,"seed_cases":3,"new_public_cases":47,
        "note":"Public evidence collection mapped by WeedDAO Research. Not industry adoption. Not FIRST_EXTERNAL_IMPLEMENTATION.",
        "first_external_implementation": False,
        "mapping_counts":{"FULL":stats["FULL_MAPPINGS"],"PARTIAL":stats["PARTIAL_MAPPINGS"],"FAILED":stats["FAILED_MAPPINGS"]},
    }
    data["REAL_WORLD_COA_MAPPINGS_COUNT"]=3
    data["PUBLIC_COA_CORPUS_V0_1_CASE_COUNT"]=50
    write_json(TRACKER, data)


# Runtime aliases bridging naming drift across incremental edits
if "sha256" not in globals() and "sha256_file" in globals():
    sha256 = sha256_file
if "write_json" not in globals() and "write_json" in globals():
    pass
if "jcode" not in globals() and "jurisdiction_code" in globals():
    jcode = jurisdiction_code
if "mk_gap" not in globals() and "make_gap" in globals():
    mk_gap = make_gap
if "empty_parsed" not in globals() and "empty_parse" in globals():
    empty_parsed = empty_parse
if "unit_schema" not in globals() and "to_schema_unit" in globals():
    unit_schema = to_schema_unit
if "RETRIEVED_AT" not in globals() and "RETRIEVED_AT" in globals():
    pass
if "CREATED_AT" not in globals() and "CREATED_AT" in globals():
    pass
if "WORKERS" not in globals() and "N_WORKERS" in globals():
    WORKERS = N_WORKERS
if "TIMEOUT" not in globals() and "FETCH_TIMEOUT" in globals():
    TIMEOUT = FETCH_TIMEOUT
if "UA" not in globals() and "USER_AGENT" in globals():
    UA = USER_AGENT
if "DOCS" not in globals() and "DOCS_DIR" in globals():
    DOCS = DOCS_DIR
if "TRACKER" not in globals() and "REVIEW_TRACKER" in globals():
    TRACKER = REVIEW_TRACKER
if "REVIEW_DATA" not in globals() and "SEED_DIR" in globals():
    REVIEW_DATA = SEED_DIR
if "map_seed" not in globals() and "map_seed_case" in globals():
    map_seed = map_seed_case
if "map_new" not in globals() and "map_new_case" in globals():
    map_new = map_new_case
if "build_source" not in globals() and "make_source" in globals():
    build_source = make_source
if "parse_source" not in globals() and "parse_case_source" in globals():
    parse_source = parse_case_source
if "panel_flags" not in globals() and "panel_flag_dict" in globals():
    panel_flags = panel_flag_dict
if "compute_stats" not in globals() and "build_stats" in globals():
    compute_stats = build_stats
if "write_docs" not in globals() and "emit_docs" in globals():
    write_docs = emit_docs
if "update_tracker" not in globals() and "patch_tracker" in globals():
    update_tracker = patch_tracker
if "validate_record" not in globals() and "validate_one" in globals():
    validate_record = validate_one
if "fetch_url" not in globals() and "fetch_one" in globals():
    fetch_url = fetch_one

def main() -> int:
    print("=== WeedDAO Public COA Corpus v0.1 build ===")
    h=sha256(SCHEMA)
    if h != EXPECTED_SHA:
        print(f"FATAL schema hash mismatch: {h}"); return 2
    print(f"OK schema sha256 {h}")
    verified=json.loads((INPUTS/"weeddao_verified_manifest_v0.1.json").read_text())
    jl=[json.loads(l) for l in (INPUTS/"weeddao_extracted_coa_data_v0.1.jsonl").read_text().splitlines() if l.strip()]
    by_id={r["case_id"]: r for r in jl}
    cases_meta=verified["cases"]
    assert len(cases_meta)==50
    write_json(INPUTS/"weeddao_extracted_coa_data_v0.1.array.json", jl)
    for d in (CASES, MAPPINGS, REVIEWS, CACHE): d.mkdir(parents=True, exist_ok=True)

    to_fetch=[c for c in cases_meta if c["case_id"] not in ("COA-001","COA-002","COA-003")]
    fetches={}
    print(f"Fetching {len(to_fetch)} sources with {WORKERS} workers...")
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs={ex.submit(fetch_url, c["case_id"], c["source_url"]): c["case_id"] for c in to_fetch}
        for fut in as_completed(futs):
            cid=futs[fut]
            try: fetches[cid]=fut.result()
            except Exception as e: fetches[cid]={"case_id":cid,"ok":False,"error":str(e),"status":None}
            st=fetches[cid]
            print(f"  {cid}: ok={st.get('ok')} status={st.get('status')} kind={st.get('kind')} err={st.get('error')}")

    manifest_rows=[]; reviews_all=[]
    for meta in cases_meta:
        case_id=meta["case_id"]; ext=by_id.get(case_id, {}); n=case_id.split("-")[1]
        print(f"Processing {case_id}...")
        if case_id in ("COA-001","COA-002","COA-003"):
            source, record, review = map_seed(case_id, meta)
            mpath=MAPPINGS/f"coa-{n}-weeddao-record.json"; write_json(mpath, record)
            valid=validate_record(mpath); review["mapped_record_valid"]=valid
            write_json(CASES/f"coa-{n}-source.json", source); write_json(REVIEWS/f"coa-{n}-review.json", review)
            flags={"has_cannabinoids":True,"has_terpenes":True,"has_microbials":True,"has_pesticides":True,"has_heavy_metals":case_id!="COA-001","has_residual_solvents":True,"has_mycotoxins":False,"has_moisture":case_id=="COA-001","has_water_activity":False,"has_foreign_material":True}
            manifest_rows.append({"case_id":case_id,"source_url":meta["source_url"],"source_tier":meta["source_tier"],"retrieved_at":RETRIEVED_AT,"jurisdiction":meta.get("jurisdiction_hint"),"producer_or_brand":source.get("producer_or_brand"),"laboratory":source.get("laboratory"),"product_name":meta.get("product_hint"),"product_type":meta.get("product_type_hint"),"batch_or_lot_id":source.get("batch_or_lot_id"),"sample_id":source.get("sample_id"),"overall_status":None,"coa_date":None,"primary_unit_types":["mg/g","%"] if case_id=="COA-001" else ["%","mg/g","mg/unit"],**flags,"has_regulatory_tracking":case_id=="COA-001","has_sample_lifecycle":case_id=="COA-001","uses_nd":case_id in ("COA-002","COA-003"),"uses_below_limit":True,"uses_not_tested":case_id=="COA-001","uses_not_reported":False,"uses_multi_unit":True,"contains_numeric_contaminant_detection":False,"contains_failure":False,"mapping_result":review["mapping_result"],"notes":"Seed hand-reviewed case"})
            reviews_all.append(review); continue

        fetch=fetches.get(case_id) or {"ok":False,"error":"missing"}
        source=build_source(case_id, meta, ext, fetch); write_json(CASES/f"coa-{n}-source.json", source)
        parsed=None
        if fetch.get("ok"):
            try: parsed=parse_source(meta["source_url"], fetch.get("text") or "", fetch.get("html"))
            except Exception as e:
                print(f"  parse error {case_id}: {e}"); traceback.print_exc(); parsed=None
        record, review = map_new(case_id, meta, ext, parsed, bool(fetch.get("ok")))
        mpath=MAPPINGS/f"coa-{n}-weeddao-record.json"; write_json(mpath, record)
        valid=validate_record(mpath); review["mapped_record_valid"]=valid
        if not valid:
            print(f"  INVALID {case_id}")
            proc=subprocess.run([str(PYTHON), str(VALIDATE), str(mpath)], capture_output=True, text=True)
            print((proc.stdout or proc.stderr or "")[-800:])
            review["mapping_result"]="FAILED"
            review["notes"]=(review.get("notes") or "")+" Record failed validate.py"
        write_json(REVIEWS/f"coa-{n}-review.json", review); reviews_all.append(review)
        flags=panel_flags(ext); units=ext.get("units_observed") or []
        notes=("SOURCE_UNAVAILABLE; " if source.get("source_unavailable") else "") + (ext.get("mapping_note") or "")
        manifest_rows.append({"case_id":case_id,"source_url":meta["source_url"],"source_tier":meta["source_tier"],"retrieved_at":RETRIEVED_AT,"jurisdiction":meta.get("jurisdiction_hint"),"producer_or_brand":source.get("producer_or_brand"),"laboratory":source.get("laboratory"),"product_name":source.get("product_name"),"product_type":source.get("product_type"),"batch_or_lot_id":source.get("batch_or_lot_id"),"sample_id":source.get("sample_id"),"overall_status":source.get("overall_status"),"coa_date":None,"primary_unit_types":units,**flags,"has_regulatory_tracking":bool(ext.get("has_metrc_or_regulatory_tracking")),"has_sample_lifecycle":bool(ext.get("has_sample_lifecycle_metadata")),"uses_nd":ext.get("uses_nd"),"uses_below_limit":ext.get("uses_below_limit"),"uses_not_tested":bool(ext.get("uses_nt_or_not_tested") or ext.get("uses_not_performed")),"uses_not_reported":ext.get("uses_nr_or_not_reported"),"uses_multi_unit":(len(units)>=2) if units else None,"contains_numeric_contaminant_detection":None,"contains_failure":str(ext.get("overall_result_observed") or "").lower().startswith("fail"),"mapping_result":review["mapping_result"],"notes":notes})

    assert len(manifest_rows)==50
    write_json(CORPUS/"manifest.json", manifest_rows)
    fields=["case_id","source_url","source_tier","retrieved_at","jurisdiction","producer_or_brand","laboratory","product_name","product_type","batch_or_lot_id","sample_id","overall_status","coa_date","primary_unit_types","has_cannabinoids","has_terpenes","has_microbials","has_pesticides","has_heavy_metals","has_residual_solvents","has_mycotoxins","has_moisture","has_water_activity","has_foreign_material","has_regulatory_tracking","has_sample_lifecycle","uses_nd","uses_below_limit","uses_not_tested","uses_not_reported","uses_multi_unit","contains_numeric_contaminant_detection","contains_failure","mapping_result","notes"]
    with (CORPUS/"manifest.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader()
        for row in manifest_rows:
            r=dict(row)
            if isinstance(r.get("primary_unit_types"), list): r["primary_unit_types"]="|".join(str(x) for x in r["primary_unit_types"])
            w.writerow(r)

    stats=compute_stats(manifest_rows, reviews_all)
    write_docs(stats); update_tracker(stats)

    print("\n=== validate.py full suite ===")
    proc=subprocess.run([str(PYTHON), str(VALIDATE)], capture_output=True, text=True)
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr); print("VALIDATION SUITE FAILED"); return 1

    bad=[]
    for rev in reviews_all:
        n=rev["case_id"].split("-")[1]; path=MAPPINGS/f"coa-{n}-weeddao-record.json"
        if rev.get("mapped_record_valid") and not validate_record(path): bad.append(rev["case_id"])
    if bad:
        print("mapped_record_valid=true but invalid:", bad); return 1

    for rev in reviews_all:
        if rev["mapping_result"]=="FULL":
            keys={g["gap_key"] for g in rev.get("gaps") or []}
            if keys & {"nd_not_representable","below_reporting_limit_qualifier","multi_unit_cannabinoid"}:
                print("QC FAIL: FULL with important dropped semantics", rev["case_id"]); return 1

    for p in CACHE.rglob("*"):
        if p.suffix.lower() in (".pdf",".png",".jpg",".jpeg",".bin"):
            try: p.unlink()
            except Exception: pass

    print("BUILD COMPLETE")
    print(json.dumps({k:stats[k] for k in ("TOTAL_CASES","FULL_MAPPINGS","PARTIAL_MAPPINGS","FAILED_MAPPINGS","SOURCE_UNAVAILABLE")}, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
