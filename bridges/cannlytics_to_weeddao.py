#!/usr/bin/env python3
"""Cannlytics LabResult → WeedDAO Cannabis Data Record v0.2-draft bridge.

Conservative semantic bridge. Documents defects; does not reshape WeedDAO schema
to fit Cannlytics. Never maps ambiguous ``nt`` → ``not_tested``. Never coerces
null cannabinoid floats to 0 / ND.

Upstream pin: cannlytics/cannabis_results @ a4e05a9f7367ac0b1637bd84773875b3bd1453ec
Bridge version: 0.2.0-compat-draft
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

BRIDGE_VERSION = "0.2.0-compat-draft"
UPSTREAM_PROJECT = "cannlytics/cannabis_results"
UPSTREAM_SCHEMA_COMMIT = "a4e05a9f7367ac0b1637bd84773875b3bd1453ec"
WEEDDAO_SCHEMA_VERSION = "0.2-draft"

# Core named cannabinoid keys in WeedDAO Cannabinoids object
CANNABINOID_CORE = {
    "delta_9_thc": "thc",
    "thc": "thc",
    "thca": "thca",
    "cbd": "cbd",
    "cbda": "cbda",
    "cbg": "cbg",
    "cbga": "cbga",
    "cbc": "cbc",
    "cbn": "cbn",
    "thcv": "thcv",
    "total_thc": "total_thc",
    "total_cbd": "total_cbd",
    "total_cannabinoids": "total_cannabinoids",
}

# Top-level LabResult percent fields that map to cannabinoids
TOP_CANNABINOID_FIELDS = [
    "delta_9_thc",
    "delta_8_thc",
    "thca",
    "total_thc",
    "cbd",
    "cbda",
    "total_cbd",
    "cbg",
    "cbga",
    "cbn",
    "cbc",
    "cbdv",
    "thcv",
    "total_cannabinoids",
]

TOP_TERPENE_FIELDS = [
    "beta_myrcene",
    "d_limonene",
    "beta_caryophyllene",
    "alpha_pinene",
    "beta_pinene",
    "linalool",
    "alpha_humulene",
    "terpinolene",
    "ocimene",
    "alpha_bisabolol",
    "camphene",
    "geraniol",
    "nerolidol",
    "guaiol",
    "caryophyllene_oxide",
]

FINISHED_PRODUCT_TOKENS = {
    "vape",
    "vaporizer",
    "cartridge",
    "cart",
    "edible",
    "gummy",
    "gummies",
    "tincture",
    "topical",
    "concentrate",
    "extract",
    "shatter",
    "wax",
    "rosin",
    "resin",
    "live_resin",
    "distillate",
    "oil",
    "preroll",
    "pre-roll",
    "pre_roll",
    "joint",
    "capsule",
    "beverage",
    "drink",
    "chocolate",
    "baked",
    "infused",
    "suppository",
    "transdermal",
    "hash",
    "kief",
    "diamonds",
    "sauce",
    "badder",
    "budder",
    "crumble",
}

FLOWERISH_TOKENS = {
    "flower",
    "bud",
    "buds",
    "biomass",
    "trim",
    "shake",
    "leaf",
    "plant",
    "hemp_flower",
    "raw_flower",
}

PANEL_FIELD_MAP = {
    "pesticides_status": "pesticides",
    "heavy_metals_status": "heavy_metals",
    "microbials_status": "microbials",
    "mycotoxins_status": "mycotoxins",
    "residual_solvents_status": "residual_solvents",
}

PASS_VALUES = {"pass", "passed", "passing", "p", "compliant", "yes", "true", "1"}
FAIL_VALUES = {"fail", "failed", "failing", "f", "non-compliant", "no", "false", "0"}
# normalize_status collapses these to 'nt' — AMBIGUOUS
NT_NORMALIZE_INPUTS = {
    "nt",
    "not tested",
    "n/t",
    "not applicable",
    "n/a",
    "na",
    "-",
    "",
}


class BridgeReport:
    def __init__(self) -> None:
        self.mapped: list[str] = []
        self.unmapped: list[str] = []
        self.gaps: dict[str, Any] = {}
        self.flags: dict[str, Any] = {
            "SUBJECT_TYPE_AMBIGUOUS": False,
            "AMBIGUOUS_NT": False,
            "PANEL_NT_AMBIGUOUS": False,
            "ND_UNRECOVERABLE": False,
            "BELOW_LIMIT_STATE_AMBIGUOUS": False,
            "LIMIT_TYPE_AMBIGUOUS": False,
            "TRACEABILITY_STRUCTURE_AMBIGUOUS": False,
            "MULTI_UNIT_PRESERVED": False,
            "STRUCTURALLY_UNMAPPABLE": False,
            "audit_class": None,
        }
        self.notes: list[str] = []

    def to_dict(self) -> dict[str, Any]:
        return {
            "mapped": self.mapped,
            "unmapped": self.unmapped,
            "gaps": self.gaps,
            "flags": self.flags,
            "notes": self.notes,
        }


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _as_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    return s if s else None


def _parse_float(v: Any) -> Optional[float]:
    if v is None or v == "":
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_datetime(v: Any) -> Optional[str]:
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return v.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    s = str(v).strip()
    if not s:
        return None
    # common ISO / date-only
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%m/%d/%Y",
    ):
        try:
            dt = datetime.strptime(s.replace("+00:00", "Z").rstrip("Z") + ("Z" if fmt.endswith("Z") and not s.endswith("Z") else ""), fmt) if False else None
        except Exception:
            dt = None
        try:
            cleaned = s
            if cleaned.endswith("Z"):
                cleaned = cleaned[:-1]
            if "+00:00" in cleaned:
                cleaned = cleaned.split("+")[0]
            dt = datetime.strptime(cleaned, fmt.rstrip("Z") if fmt.endswith("Z") else fmt)
            return dt.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None


def _normalize_token(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def _is_finished_product(product_type: Optional[str]) -> bool:
    if not product_type:
        return False
    tok = _normalize_token(product_type)
    parts = set(tok.split("_"))
    if tok in FINISHED_PRODUCT_TOKENS:
        return True
    if parts & FINISHED_PRODUCT_TOKENS:
        return True
    for t in FINISHED_PRODUCT_TOKENS:
        if t in tok:
            return True
    return False


def _is_flowerish(product_type: Optional[str]) -> bool:
    if not product_type:
        return False
    tok = _normalize_token(product_type)
    for t in FLOWERISH_TOKENS:
        if t in tok:
            return True
    return False


def _harvest_lot_supported(src: dict[str, Any]) -> bool:
    """Only true when metadata clearly indicates harvest/lot semantics."""
    hints = []
    for k in ("product_subtype", "product_type", "batch_number"):
        v = _as_str(src.get(k))
        if v:
            hints.append(v.lower())
    blob = " ".join(hints)
    return bool(re.search(r"\b(harvest|lot|harvest_lot|harvest-lot)\b", blob))


def _status_bucket(raw: Any) -> tuple[Optional[str], Optional[str]]:
    """Return (bucket, raw_str) where bucket in pass|fail|nt_ambiguous|explicit_not_tested|explicit_not_applicable|other|None."""
    if raw is None:
        return None, None
    raw_str = str(raw).strip()
    if raw_str == "":
        return "nt_ambiguous", raw_str
    low = raw_str.lower().strip()
    if low in PASS_VALUES:
        return "pass", raw_str
    if low in FAIL_VALUES:
        return "fail", raw_str
    # Explicit full phrases BEFORE collapsing to nt
    if low in {"not tested", "not_tested", "not-tested"}:
        return "explicit_not_tested", raw_str
    if low in {"not applicable", "not_applicable", "not-applicable"}:
        return "explicit_not_applicable", raw_str
    if low in NT_NORMALIZE_INPUTS or low == "nt":
        return "nt_ambiguous", raw_str
    return "other", raw_str


def _detected_measurement(value: float, unit: str) -> dict[str, Any]:
    return {
        "result_state": "detected",
        "measurements": [{"value": value, "unit": unit}],
        "provenance": "derived",
    }


def _merge_measurement(ar: dict[str, Any], value: float, unit: str) -> dict[str, Any]:
    ar = deepcopy(ar)
    ar.setdefault("measurements", [])
    # avoid duplicate same unit
    for m in ar["measurements"]:
        if m.get("unit") == unit:
            return ar
    ar["measurements"].append({"value": value, "unit": unit})
    return ar


def _parse_results_list(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [x for x in raw if isinstance(x, dict)]
    if isinstance(raw, str):
        s = raw.strip()
        if not s:
            return []
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                return [x for x in parsed if isinstance(x, dict)]
        except json.JSONDecodeError:
            pass
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, list):
                return [x for x in parsed if isinstance(x, dict)]
        except (ValueError, SyntaxError):
            pass
    return []


def _value_kind(value: Any) -> dict[str, Any]:
    """Classify a ResultDetail value for mapping."""
    info: dict[str, Any] = {
        "numeric": None,
        "explicit_nd": False,
        "explicit_nt": False,
        "explicit_not_tested": False,
        "explicit_na": False,
        "below_loq": False,
        "below_lod": False,
        "raw": value,
    }
    if value is None:
        return info
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        info["numeric"] = float(value)
        return info
    s = str(value).strip()
    if not s:
        return info
    low = s.lower()
    if low in {"nd", "n.d.", "not detected", "not_detected", "non-detect", "nondetect"}:
        info["explicit_nd"] = True
        return info
    if low in {"not tested", "not_tested"}:
        info["explicit_not_tested"] = True
        return info
    if low in {"nt"}:
        info["explicit_nt"] = True
        return info
    if low in {"n/a", "na", "not applicable", "not_applicable"}:
        info["explicit_na"] = True
        return info
    m = re.match(r"^<\s*(loq|lod)\s*$", low)
    if m:
        if m.group(1) == "loq":
            info["below_loq"] = True
        else:
            info["below_lod"] = True
        return info
    m2 = re.match(r"^<\s*([0-9]*\.?[0-9]+)\s*$", s)
    if m2:
        info["below_loq"] = True  # generic less-than numeric — treat as below reporting
        info["numeric"] = float(m2.group(1))
        info["lt_numeric"] = True
        return info
    num = _parse_float(s)
    if num is not None:
        info["numeric"] = num
    return info


def convert_lab_result(src: dict[str, Any]) -> tuple[Optional[dict[str, Any]], dict[str, Any]]:
    """Convert a Cannlytics LabResult-shaped dict to WeedDAO v0.2-draft.

    Returns (record_or_None, bridge_report_dict).
    """
    report = BridgeReport()
    src = dict(src or {})

    # --- identity / subject_id ---
    upstream_id = _as_str(src.get("id"))
    batch_number = _as_str(src.get("batch_number"))
    sample_id = _as_str(src.get("sample_id"))
    subject_id = batch_number or sample_id or upstream_id
    if not subject_id:
        report.flags["STRUCTURALLY_UNMAPPABLE"] = True
        report.flags["audit_class"] = "STRUCTURALLY_UNMAPPABLE"
        report.gaps["subject_id"] = "missing_batch_number_sample_id_and_id"
        report.notes.append("STRUCTURALLY_UNMAPPABLE: no subject_id candidate")
        return None, report.to_dict()

    if upstream_id:
        record_id = upstream_id
        report.mapped.append("id→record_id")
    else:
        digest = hashlib.sha256(
            json.dumps(
                {
                    "subject_id": subject_id,
                    "product_name": src.get("product_name"),
                    "date_tested": str(src.get("date_tested")),
                    "source": src.get("source"),
                },
                sort_keys=True,
                default=str,
            ).encode()
        ).hexdigest()[:16]
        record_id = f"weeddao-bridge-{digest}"
        report.notes.append("record_id is bridge-generated (upstream id absent); not an upstream identifier")
        report.gaps["record_id_generated"] = "bridge_deterministic"

    product_type = _as_str(src.get("product_type"))
    product_name = _as_str(src.get("product_name"))
    product_subtype = _as_str(src.get("product_subtype"))

    # --- subject_type (conservative) ---
    subject_type: str
    if _is_finished_product(product_type):
        subject_type = "product_batch"
        report.mapped.append("product_type→subject.subject_type=product_batch")
    elif sample_id and not batch_number and not _is_finished_product(product_type) and not _is_flowerish(product_type):
        # only sample identity strongly indicated
        subject_type = "sample"
        report.mapped.append("sample_id-only→subject.subject_type=sample")
    elif _is_flowerish(product_type):
        if _harvest_lot_supported(src):
            subject_type = "harvest_lot"
            report.mapped.append("flower+harvest/lot metadata→subject.subject_type=harvest_lot")
        else:
            subject_type = "other"
            report.flags["SUBJECT_TYPE_AMBIGUOUS"] = True
            report.gaps["subject_type"] = "flowerish_without_harvest_lot_metadata"
            report.notes.append(
                "SUBJECT_TYPE_AMBIGUOUS: flower/bud/biomass without harvest/lot metadata; "
                "using subject_type=other (not cultivation_batch)"
            )
    elif sample_id and not product_type:
        subject_type = "sample"
        report.mapped.append("sample_id without product_type→subject.subject_type=sample")
    else:
        subject_type = "other"
        report.flags["SUBJECT_TYPE_AMBIGUOUS"] = True
        report.gaps["subject_type"] = "indeterminate_product_type"
        report.notes.append("SUBJECT_TYPE_AMBIGUOUS: product_type not clearly finished/flower/sample")

    subject: dict[str, Any] = {
        "subject_type": subject_type,
        "subject_id": subject_id,
    }
    if product_name:
        subject["name"] = product_name
        report.mapped.append("product_name→subject.name")
    if product_type:
        subject["product_type"] = product_type
        report.mapped.append("product_type→subject.product_type")
    if product_subtype:
        subject["matrix"] = product_subtype
        report.mapped.append("product_subtype→subject.matrix")

    # external identifiers / metrc
    ext_ids: list[dict[str, Any]] = []
    if _as_str(src.get("metrc_lab_id")):
        ext_ids.append({"scheme": "metrc.lab", "value": _as_str(src.get("metrc_lab_id")), "scope": "sample"})
        report.mapped.append("metrc_lab_id→external_identifiers[metrc.lab]")
    if _as_str(src.get("metrc_source_id")):
        ext_ids.append({"scheme": "metrc.source", "value": _as_str(src.get("metrc_source_id")), "scope": "source"})
        report.mapped.append("metrc_source_id→external_identifiers[metrc.source]")
    metrc_ids = src.get("metrc_ids") or []
    if isinstance(metrc_ids, str):
        try:
            metrc_ids = json.loads(metrc_ids)
        except json.JSONDecodeError:
            try:
                metrc_ids = ast.literal_eval(metrc_ids)
            except Exception:
                metrc_ids = [metrc_ids] if metrc_ids.strip() else []
    if isinstance(metrc_ids, list):
        for mid in metrc_ids:
            mv = _as_str(mid)
            if mv:
                ext_ids.append({"scheme": "metrc.tag", "value": mv, "scope": "package"})
        if metrc_ids:
            report.mapped.append("metrc_ids→external_identifiers[metrc.tag]")
    # ambiguous traceability_ids
    tid = src.get("traceability_ids")
    if tid:
        report.flags["TRACEABILITY_STRUCTURE_AMBIGUOUS"] = True
        report.gaps["traceability_ids"] = "TRACEABILITY_STRUCTURE_AMBIGUOUS"
        report.unmapped.append("traceability_ids")

    if sample_id:
        ext_ids.append({"scheme": "lab.sample", "value": sample_id, "scope": "sample"})
        report.mapped.append("sample_id→external_identifiers[lab.sample]")

    if ext_ids:
        subject["external_identifiers"] = ext_ids

    record: dict[str, Any] = {
        "schema_version": WEEDDAO_SCHEMA_VERSION,
        "record_id": record_id,
        "created_at": _parse_datetime(src.get("created_at")) or _now_iso(),
        "subject": subject,
    }
    if _parse_datetime(src.get("updated_at")):
        record["updated_at"] = _parse_datetime(src.get("updated_at"))

    # producer
    producer_name = _as_str(src.get("producer"))
    producer_license = _as_str(src.get("producer_license_number"))
    producer_state = _as_str(src.get("producer_state")) or _as_str(src.get("state"))
    if producer_name or producer_license:
        producer: dict[str, Any] = {}
        if producer_name:
            producer["organization_name"] = producer_name
            report.mapped.append("producer→producer.organization_name")
        if producer_license:
            producer["license_id"] = producer_license
            report.mapped.append("producer_license_number→producer.license_id")
        if producer_state:
            producer["jurisdiction"] = producer_state
            report.mapped.append("state/producer_state→producer.jurisdiction")
        # address kept conservative — stash in extension, not forced into core
        addr_bits = {
            k: _as_str(src.get(k))
            for k in (
                "producer_address",
                "producer_street",
                "producer_city",
                "producer_zipcode",
            )
            if _as_str(src.get(k))
        }
        if addr_bits:
            report.notes.append("producer address fields preserved in extensions (conservative core mapping)")
        record["producer"] = producer

    # cultivar — strain_name ONLY
    strain = _as_str(src.get("strain_name"))
    if strain:
        record["cultivar"] = {
            "reported_name": strain,
            "identity_status": "reported",
        }
        report.mapped.append("strain_name→cultivar.reported_name")
    else:
        # do NOT derive from product_name / classification / indica% / sativa%
        for forbidden in ("classification", "indica_percentage", "sativa_percentage", "product_name"):
            if src.get(forbidden) not in (None, ""):
                report.unmapped.append(f"{forbidden} (not used for cultivar)")

    # lab_results
    lab_results: dict[str, Any] = {"provenance": "derived"}
    lab_name = _as_str(src.get("lab"))
    if lab_name:
        lab_results["lab_name"] = lab_name
        report.mapped.append("lab→lab_results.lab_name")
    lab_id = _as_str(src.get("lab_id"))
    if lab_id:
        lab_results["lab_id"] = lab_id
        report.mapped.append("lab_id→lab_results.lab_id")
    if sample_id:
        lab_results["sample_id"] = sample_id

    # lifecycle dates — never manufacture reported_at
    sample_life: dict[str, Any] = {}
    if sample_id:
        sample_life["sample_id"] = sample_id
    collected = _parse_datetime(src.get("date_collected") or src.get("date_sampled"))
    if collected:
        sample_life["collected_at"] = collected
        report.mapped.append("date_collected→lab_results.sample.collected_at")
    received = _parse_datetime(src.get("date_received"))
    if received:
        sample_life["received_at"] = received
        report.mapped.append("date_received→lab_results.sample.received_at")
    produced = _parse_datetime(src.get("date_produced"))
    if produced:
        sample_life["produced_at"] = produced
        report.mapped.append("date_produced→lab_results.sample.produced_at")
    if product_subtype:
        sample_life["matrix"] = product_subtype
    if sample_life:
        lab_results["sample"] = sample_life

    tested = _parse_datetime(src.get("date_tested"))
    if tested:
        lab_results["tested_at"] = tested
        report.mapped.append("date_tested→lab_results.tested_at")

    # best_by: date_expires ONLY when equivalence is supportable — we omit by default
    # (expiration ≠ best-by without source confirmation)
    if src.get("date_expires") not in (None, ""):
        report.unmapped.append("date_expires (not mapped to best_by; equivalence unsupported)")
        report.gaps["date_expires"] = "equivalence_to_best_by_unsupported"

    # cannabinoids from top-level floats
    cannabinoids: dict[str, Any] = {}
    other_cann: list[dict[str, Any]] = []

    def put_cannabinoid(key: str, value: float, unit: str = "%") -> None:
        nonlocal cannabinoids, other_cann
        core = CANNABINOID_CORE.get(key)
        if core:
            existing = cannabinoids.get(core)
            if existing and existing.get("result_state") == "detected":
                cannabinoids[core] = _merge_measurement(existing, value, unit)
                if unit == "mg/g":
                    report.flags["MULTI_UNIT_PRESERVED"] = True
            else:
                cannabinoids[core] = _detected_measurement(value, unit)
            report.mapped.append(f"{key}→lab_results.cannabinoids.{core}")
        else:
            # find or create in other
            name = key
            found = None
            for item in other_cann:
                if item.get("name") == name and item.get("result_state") == "detected":
                    found = item
                    break
            if found:
                updated = _merge_measurement(found, value, unit)
                found.clear()
                found.update(updated)
                found["name"] = name
                if unit == "mg/g":
                    report.flags["MULTI_UNIT_PRESERVED"] = True
            else:
                ar = _detected_measurement(value, unit)
                ar["name"] = name
                other_cann.append(ar)
            report.mapped.append(f"{key}→lab_results.cannabinoids.other[{name}]")

    for field in TOP_CANNABINOID_FIELDS:
        if field not in src:
            continue
        raw_v = src.get(field)
        if raw_v is None or raw_v == "":
            # null/absent — do NOT coerce to 0 or ND
            report.gaps[f"null_float:{field}"] = "omitted_ambiguous_null"
            report.flags["ND_UNRECOVERABLE"] = True
            report.notes.append(
                f"ND_UNRECOVERABLE/null: top-level {field} is null/empty — omitted "
                "(missing vs ND vs not tested indistinguishable in normalized float)"
            )
            continue
        num = _parse_float(raw_v)
        if num is None:
            report.unmapped.append(f"{field} (non-numeric)")
            continue
        put_cannabinoid(field, num, "%")

    # terpenes top-level
    terpenes: list[dict[str, Any]] = []
    for field in TOP_TERPENE_FIELDS:
        if field not in src:
            continue
        raw_v = src.get(field)
        if raw_v is None or raw_v == "":
            report.gaps[f"null_float:{field}"] = "omitted_ambiguous_null"
            continue
        num = _parse_float(raw_v)
        if num is None:
            continue
        terpenes.append(
            {
                "name": field,
                "result_state": "detected",
                "measurements": [{"value": num, "unit": "%"}],
                "provenance": "derived",
            }
        )
        report.mapped.append(f"{field}→lab_results.terpenes")
    if "total_terpenes" in src and src.get("total_terpenes") not in (None, ""):
        num = _parse_float(src.get("total_terpenes"))
        if num is not None:
            lab_results["total_terpenes"] = _detected_measurement(num, "%")
            report.mapped.append("total_terpenes→lab_results.total_terpenes")

    # moisture / water activity
    if src.get("moisture_content") not in (None, ""):
        num = _parse_float(src.get("moisture_content"))
        if num is not None:
            lab_results["moisture"] = _detected_measurement(num, "%")
            report.mapped.append("moisture_content→lab_results.moisture")
    if src.get("water_activity") not in (None, ""):
        num = _parse_float(src.get("water_activity"))
        if num is not None:
            lab_results["water_activity"] = _detected_measurement(num, "aw")
            report.mapped.append("water_activity→lab_results.water_activity")

    # results[] ResultDetail
    details = _parse_results_list(src.get("results"))
    safety_analytes: dict[str, list[dict[str, Any]]] = {
        "pesticides": [],
        "heavy_metals": [],
        "microbials": [],
        "mycotoxins": [],
        "residual_solvents": [],
    }
    analysis_to_panel = {
        "pesticides": "pesticides",
        "pesticide": "pesticides",
        "heavy_metals": "heavy_metals",
        "heavy metals": "heavy_metals",
        "metals": "heavy_metals",
        "microbials": "microbials",
        "microbes": "microbials",
        "microbial": "microbials",
        "mycotoxins": "mycotoxins",
        "mycotoxin": "mycotoxins",
        "residual_solvents": "residual_solvents",
        "residual solvents": "residual_solvents",
        "solvents": "residual_solvents",
    }

    for det in details:
        key = _as_str(det.get("key")) or _as_str(det.get("name")) or "unknown"
        name = _as_str(det.get("name")) or key
        analysis = (_as_str(det.get("analysis")) or "").lower()
        units = _as_str(det.get("units")) or "%"
        status_raw = det.get("status")
        status_bucket, status_str = _status_bucket(status_raw)
        vk = _value_kind(det.get("value"))
        mg_g = _parse_float(det.get("mg_g"))
        lod = _parse_float(det.get("lod"))
        loq = _parse_float(det.get("loq"))
        limit_raw = det.get("limit")
        limit_num = _parse_float(limit_raw)

        ar: dict[str, Any] = {"name": name}

        # assessment from status ONLY — never auto-set result_state from pass/fail
        if status_bucket == "pass":
            ar["assessment"] = "pass"
        elif status_bucket == "fail":
            ar["assessment"] = "fail"

        limits: list[dict[str, Any]] = []
        if lod is not None:
            limits.append({"type": "LOD", "value": lod, "unit": units})
            report.mapped.append(f"results[].lod→limits[LOD] ({key})")
        if loq is not None:
            limits.append({"type": "LOQ", "value": loq, "unit": units})
            report.mapped.append(f"results[].loq→limits[LOQ] ({key})")
        if limit_num is not None:
            limits.append(
                {
                    "type": "other",
                    "value": limit_num,
                    "unit": units,
                    "notes": "Cannlytics generic ResultDetail.limit; type ambiguous",
                }
            )
            report.flags["LIMIT_TYPE_AMBIGUOUS"] = True
            report.gaps[f"limit:{key}"] = "LIMIT_TYPE_AMBIGUOUS"

        # result_state logic
        if vk["explicit_nd"]:
            ar["result_state"] = "not_detected"
            ar["reported_as"] = str(det.get("value"))
            report.mapped.append(f"results[] ND→not_detected ({key})")
        elif vk["explicit_not_tested"]:
            ar["result_state"] = "not_tested"
            ar["reported_as"] = str(det.get("value"))
            report.mapped.append(f"results[] 'Not Tested'→not_tested ({key})")
        elif vk["explicit_na"]:
            ar["result_state"] = "not_applicable"
            ar["reported_as"] = str(det.get("value"))
        elif vk["explicit_nt"] or status_bucket == "nt_ambiguous":
            # DO NOT map to not_tested
            ar["result_state"] = "unknown"
            ar["reported_as"] = "nt" if vk["explicit_nt"] or (status_str or "").lower() == "nt" else (status_str or "nt")
            ar["notes"] = (
                "Cannlytics status/value 'nt' is ambiguous "
                "(normalize_status maps not tested / n/a / na / '-' / '' → nt). "
                "Not mapped to WeedDAO not_tested."
            )
            report.flags["AMBIGUOUS_NT"] = True
            report.gaps[f"nt:{key}"] = "AMBIGUOUS_NT"
            report.notes.append(f"AMBIGUOUS_NT for analyte {key}")
        elif vk.get("below_loq") or vk.get("below_lod"):
            ar["result_state"] = "below_reporting_limit"
            ar["reported_as"] = str(det.get("value"))
            if not limits:
                # still valid via reported_as
                pass
            report.mapped.append(f"results[] <LOQ/<LOD→below_reporting_limit ({key})")
        elif vk["numeric"] is not None and not vk.get("lt_numeric"):
            ar["result_state"] = "detected"
            ar["measurements"] = [{"value": vk["numeric"], "unit": units}]
            if mg_g is not None:
                ar = _merge_measurement(ar, mg_g, "mg/g")
                report.flags["MULTI_UNIT_PRESERVED"] = True
            report.mapped.append(f"results[] value→detected ({key})")
        elif vk.get("lt_numeric"):
            ar["result_state"] = "below_reporting_limit"
            ar["reported_as"] = str(det.get("value"))
            if limits:
                ar["limits"] = limits
            elif vk["numeric"] is not None:
                ar["limits"] = [{"type": "reporting_limit", "operator": "<", "value": vk["numeric"], "unit": units}]
            report.mapped.append(f"results[] <N→below_reporting_limit ({key})")
        elif det.get("value") is None:
            # null without ND text
            if lod is not None or loq is not None:
                # LOQ/LOD present without below qualifier — DO NOT infer below_limit
                ar["result_state"] = "unknown"
                ar["notes"] = (
                    "LOQ/LOD present without explicit below-limit qualifier; "
                    "not inferred as below_reporting_limit"
                )
                if limits:
                    ar["limits"] = limits
                report.flags["BELOW_LIMIT_STATE_AMBIGUOUS"] = True
                report.gaps[f"below_limit:{key}"] = "BELOW_LIMIT_STATE_AMBIGUOUS"
            else:
                ar["result_state"] = "unknown"
                ar["notes"] = "Null value without ND/NT qualifier; ND_UNRECOVERABLE"
                report.flags["ND_UNRECOVERABLE"] = True
                report.gaps[f"null_value:{key}"] = "ND_UNRECOVERABLE"
        else:
            ar["result_state"] = "unknown"
            ar["reported_as"] = str(det.get("value"))
            report.notes.append(f"unclassified ResultDetail value for {key}")

        if limits and "limits" not in ar:
            ar["limits"] = limits
        if mg_g is not None and ar.get("result_state") == "detected":
            ar = _merge_measurement(ar, mg_g, "mg/g")
            report.flags["MULTI_UNIT_PRESERVED"] = True
            ar["name"] = name

        # route by analysis
        if analysis in {"cannabinoids", "cannabinoid", "potency"}:
            put_key = key
            # map standard keys
            core = CANNABINOID_CORE.get(put_key) or CANNABINOID_CORE.get(put_key.replace("-", "_"))
            if ar.get("result_state") == "detected" and ar.get("measurements"):
                for m in ar["measurements"]:
                    put_cannabinoid(put_key if not core else (put_key if put_key in CANNABINOID_CORE else put_key), m["value"], m["unit"])
                # if put_cannabinoid used key path; for non-detected states put as other
            else:
                # non-detected or unknown — go to other with full AnalyteResult
                item = {k: v for k, v in ar.items()}
                other_cann.append(item)
        elif analysis in {"terpenes", "terpene"}:
            item = {k: v for k, v in ar.items()}
            terpenes.append(item)
        elif analysis in analysis_to_panel:
            panel = analysis_to_panel[analysis]
            safety_analytes[panel].append(ar)
        else:
            # stash under extensions later via other_cann-like? keep as unmapped detail note
            report.unmapped.append(f"results[] analysis={analysis!r} key={key}")

    if other_cann:
        cannabinoids["other"] = other_cann
    if cannabinoids:
        lab_results["cannabinoids"] = cannabinoids
    if terpenes:
        lab_results["terpenes"] = terpenes

    # panel statuses
    safety: dict[str, Any] = {}
    panel_nt_meta: dict[str, Any] = {}
    for src_field, panel_key in PANEL_FIELD_MAP.items():
        if src_field not in src and src.get(src_field) is None:
            # still check presence
            if src_field not in src:
                continue
        raw = src.get(src_field)
        if raw is None or raw == "":
            continue
        bucket, raw_str = _status_bucket(raw)
        panel_obj: dict[str, Any] = {}
        if safety_analytes.get(panel_key):
            panel_obj["analytes"] = safety_analytes[panel_key]
        if bucket == "pass":
            panel_obj["status"] = "pass"
            safety[panel_key] = panel_obj
            report.mapped.append(f"{src_field}→safety.{panel_key}.status=pass")
        elif bucket == "fail":
            panel_obj["status"] = "fail"
            safety[panel_key] = panel_obj
            report.mapped.append(f"{src_field}→safety.{panel_key}.status=fail")
        elif bucket == "explicit_not_tested":
            panel_obj["status"] = "not_tested"
            panel_obj["notes"] = f"Source reported {raw_str!r}"
            safety[panel_key] = panel_obj
        elif bucket == "explicit_not_applicable":
            panel_obj["status"] = "not_applicable"
            safety[panel_key] = panel_obj
        elif bucket == "nt_ambiguous":
            # OMIT WeedDAO panel status; preserve nt in compat metadata
            report.flags["PANEL_NT_AMBIGUOUS"] = True
            panel_nt_meta[panel_key] = {"cannlytics_status": raw_str or "nt"}
            report.gaps[f"panel_nt:{panel_key}"] = "PANEL_NT_AMBIGUOUS"
            report.notes.append(
                f"PANEL_NT_AMBIGUOUS: {src_field}={raw_str!r} omitted from WeedDAO panel status"
            )
            if panel_obj.get("analytes"):
                # keep analytes without status
                safety[panel_key] = {"analytes": panel_obj["analytes"], "notes": "Panel status omitted due to ambiguous Cannlytics nt"}
        else:
            report.unmapped.append(f"{src_field}={raw_str!r}")

    # attach analytes even if no panel status field
    for panel_key, analytes in safety_analytes.items():
        if analytes and panel_key not in safety:
            safety[panel_key] = {"analytes": analytes}

    if safety:
        lab_results["safety"] = safety

    # foreign_matter_status — AnalyteResult-ish, not SafetyPanel in WeedDAO
    fms = src.get("foreign_matter_status")
    if fms not in (None, ""):
        bucket, raw_str = _status_bucket(fms)
        if bucket == "pass":
            lab_results["foreign_material"] = {
                "result_state": "unknown",
                "assessment": "pass",
                "reported_as": raw_str,
                "notes": "Panel/visual status only; no numeric foreign-material measurement",
            }
            report.mapped.append("foreign_matter_status→foreign_material (assessment only)")
        elif bucket == "fail":
            lab_results["foreign_material"] = {
                "result_state": "unknown",
                "assessment": "fail",
                "reported_as": raw_str,
            }
        elif bucket == "nt_ambiguous":
            report.flags["PANEL_NT_AMBIGUOUS"] = True
            panel_nt_meta["foreign_matter"] = {"cannlytics_status": raw_str or "nt"}
            report.gaps["panel_nt:foreign_matter"] = "PANEL_NT_AMBIGUOUS"
        else:
            report.unmapped.append(f"foreign_matter_status={raw_str!r}")

    record["lab_results"] = lab_results

    # overall_status → outcomes/extension only
    overall = src.get("overall_status")
    outcomes: dict[str, Any] = {}
    if overall not in (None, ""):
        outcomes["cannlytics_overall_status"] = str(overall)
        report.mapped.append("overall_status→outcomes.cannlytics_overall_status (not panel fail)")
        report.notes.append("overall_status not mapped onto individual WeedDAO panel statuses")

    if outcomes:
        record["outcomes"] = outcomes

    # extensions
    extensions: dict[str, Any] = {
        "cannlytics_bridge": {
            "upstream_project": UPSTREAM_PROJECT,
            "upstream_record_id": upstream_id,
            "upstream_source": _as_str(src.get("source")),
            "upstream_schema_commit": UPSTREAM_SCHEMA_COMMIT,
            "bridge_version": BRIDGE_VERSION,
            "panel_nt_preserved": panel_nt_meta or None,
            "flags": {k: v for k, v in report.flags.items() if v},
        }
    }
    # stash address / distributor / coa urls etc.
    stash = {}
    for k in (
        "distributor",
        "distributor_license_number",
        "distributor_address",
        "producer_address",
        "producer_street",
        "producer_city",
        "producer_zipcode",
        "lab_address",
        "lab_license_number",
        "lab_state",
        "coa_url",
        "coa_urls",
        "coa_pdf",
        "lab_results_url",
        "images",
        "classification",
        "indica_percentage",
        "sativa_percentage",
        "batch_size",
        "product_size",
        "serving_size",
        "servings_per_package",
        "state",
        "data_refreshed_date",
        "sample_hash",
        "results_hash",
        "date_packaged",
        "date_expires",
        "traceability_ids",
    ):
        if src.get(k) not in (None, "", [], {}):
            stash[k] = src.get(k)
            if k not in report.mapped and k not in report.unmapped:
                report.unmapped.append(k)
    if stash:
        extensions["cannlytics_source_fields"] = stash
    record["extensions"] = extensions

    # audit class
    if report.flags["STRUCTURALLY_UNMAPPABLE"]:
        report.flags["audit_class"] = "STRUCTURALLY_UNMAPPABLE"
    elif any(
        report.flags[f]
        for f in (
            "SUBJECT_TYPE_AMBIGUOUS",
            "AMBIGUOUS_NT",
            "PANEL_NT_AMBIGUOUS",
            "ND_UNRECOVERABLE",
            "BELOW_LIMIT_STATE_AMBIGUOUS",
            "LIMIT_TYPE_AMBIGUOUS",
            "TRACEABILITY_STRUCTURE_AMBIGUOUS",
        )
    ):
        report.flags["audit_class"] = "SEMANTICALLY_PARTIAL"
    else:
        report.flags["audit_class"] = "LOSSLESS_FOR_AVAILABLE_SEMANTICS"
        report.notes.append(
            "LOSSLESS_FOR_AVAILABLE_SEMANTICS means all semantics present in the "
            "Cannlytics *normalized* record were represented without guessing — "
            "NOT that the original COA was lossless."
        )

    # data_gaps for schema gap markers (optional)
    data_gaps = {}
    if report.gaps.get("subject_type"):
        data_gaps["subject.subject_type_precision"] = "not_measured"
    if data_gaps:
        record["data_gaps"] = data_gaps

    return record, report.to_dict()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Cannlytics → WeedDAO v0.2-draft bridge")
    parser.add_argument("input", type=Path, help="Cannlytics LabResult JSON file")
    parser.add_argument("-o", "--output", type=Path, help="Write WeedDAO record JSON")
    parser.add_argument("--report", type=Path, help="Write bridge_report JSON")
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args(argv)

    src = load_json(args.input)
    if isinstance(src, list):
        print("ERROR: expected a single LabResult object, not a list", file=sys.stderr)
        return 2
    record, report = convert_lab_result(src)
    if record is None:
        print(json.dumps({"error": "STRUCTURALLY_UNMAPPABLE", "report": report}, indent=args.indent))
        if args.report:
            args.report.write_text(json.dumps(report, indent=args.indent), encoding="utf-8")
        return 1
    text = json.dumps(record, indent=args.indent)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if args.report:
        args.report.write_text(json.dumps(report, indent=args.indent) + "\n", encoding="utf-8")
    else:
        print(json.dumps({"bridge_report": report}, indent=args.indent), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
