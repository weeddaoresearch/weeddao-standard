"""Map parsed COA + extraction metadata → WeedDAO v0.1-alpha record + review."""
from __future__ import annotations

import copy
from typing import Any

from common import CANN_KEYS, CREATED_AT, jurisdiction_code, load_json, REVIEW_DATA

SEED_GAPS = {
    "COA-001": [
        {"gap_key": "below_reporting_limit_qualifier", "observed_source_semantics": "Cannabinoid/terpene results as <0.1 mg/g or <0.01%", "severity": "CRITICAL_INTEROPERABILITY", "existing_issue_if_any": 1},
        {"gap_key": "analyte_level_not_performed", "observed_source_semantics": "P. aeruginosa Not Performed; residual solvents Not Performed", "severity": "CRITICAL_INTEROPERABILITY", "existing_issue_if_any": 2},
        {"gap_key": "extended_cannabinoid_vocabulary", "observed_source_semantics": "Δ8/Δ10/THCP/CBDV on COA", "severity": "IMPORTANT", "existing_issue_if_any": None},
        {"gap_key": "sample_lifecycle_metadata", "observed_source_semantics": "Date received / collected-by not first-class", "severity": "IMPORTANT", "existing_issue_if_any": None},
        {"gap_key": "foreign_material", "observed_source_semantics": "Passed Visual Inspection", "severity": "IMPORTANT", "existing_issue_if_any": None},
        {"gap_key": "multi_unit_cannabinoid", "observed_source_semantics": "Totals in mg/g and %", "severity": "CRITICAL_INTEROPERABILITY", "existing_issue_if_any": 4},
        {"gap_key": "moisture_not_in_core", "observed_source_semantics": "Moisture Not Performed", "severity": "OPTIONAL", "existing_issue_if_any": None},
    ],
    "COA-002": [
        {"gap_key": "nd_not_representable", "observed_source_semantics": "Multiple cannabinoid/terpene ND", "severity": "CRITICAL_INTEROPERABILITY", "existing_issue_if_any": 3},
        {"gap_key": "below_reporting_limit_qualifier", "observed_source_semantics": "Heavy metals <0.008 ppm", "severity": "CRITICAL_INTEROPERABILITY", "existing_issue_if_any": 1},
        {"gap_key": "multi_unit_cannabinoid", "observed_source_semantics": "%wt + mg/g + mg/unit", "severity": "CRITICAL_INTEROPERABILITY", "existing_issue_if_any": 4},
        {"gap_key": "foreign_material", "observed_source_semantics": "Visual Inspection Passed", "severity": "IMPORTANT", "existing_issue_if_any": None},
        {"gap_key": "best_by_date", "observed_source_semantics": "Best by on COA", "severity": "OPTIONAL", "existing_issue_if_any": None},
    ],
    "COA-003": [
        {"gap_key": "nd_not_representable", "observed_source_semantics": "Multiple cannabinoid/terpene ND", "severity": "CRITICAL_INTEROPERABILITY", "existing_issue_if_any": 3},
        {"gap_key": "below_reporting_limit_qualifier", "observed_source_semantics": "Heavy metals <0.008 ppm", "severity": "CRITICAL_INTEROPERABILITY", "existing_issue_if_any": 1},
        {"gap_key": "multi_unit_cannabinoid", "observed_source_semantics": "%wt + mg/g + mg/unit", "severity": "CRITICAL_INTEROPERABILITY", "existing_issue_if_any": 4},
        {"gap_key": "literal_batch_id_zero", "observed_source_semantics": "Batch ID literal '0'", "severity": "IMPORTANT", "existing_issue_if_any": None},
        {"gap_key": "foreign_material", "observed_source_semantics": "Visual Inspection Passed", "severity": "IMPORTANT", "existing_issue_if_any": None},
    ],
}


def gap(key, semantics, severity, issue=None):
    return {
        "gap_key": key,
        "observed_source_semantics": semantics,
        "severity": severity,
        "existing_issue_if_any": issue,
    }


def unit_to_schema(unit: str) -> str | None:
    u = (unit or "%").strip().lower().replace("ml", "ml")
    if u in ("%", "percent"):
        return "%"
    if u in ("mg/g",):
        return "mg/g"
    if u in ("mg/ml", "mg/ml"):
        return "mg/ml"
    if u in ("mg/serving", "mg/unit", "mg/srv"):
        return "mg/serving"
    return None


def map_seed(case_id: str, meta: dict, ext: dict) -> tuple[dict, dict, dict]:
    n = case_id.split("-")[1]
    record = load_json(REVIEW_DATA / f"coa-{n}-weeddao-record.json")
    source = {
        "case_id": case_id,
        "source_url": meta["source_url"],
        "source_tier": meta["source_tier"],
        "source_group": meta.get("source_group"),
        "jurisdiction_hint": meta.get("jurisdiction_hint"),
        "product_hint": meta.get("product_hint"),
        "product_type_hint": meta.get("product_type_hint"),
        "seed_reuse": True,
        "laboratory": {"COA-001": "external-lab-001", "COA-002": "external-lab-002", "COA-003": "external-lab-002"}[case_id],
        "producer_or_brand": {"COA-001": "Desert Green Farm", "COA-002": "Texas Original", "COA-003": "Texas Original"}[case_id],
        "batch_or_lot_id": record.get("cultivation_batch_id"),
        "sample_id": (record.get("lab_results") or {}).get("sample_id"),
        "detail_level": "high",
        "notes": "Seed case: reused hand-reviewed WeedDAO mapping; original COA image not republished.",
    }
    gaps = copy.deepcopy(SEED_GAPS[case_id])
    exact = {"COA-001": 12, "COA-002": 14, "COA-003": 13}[case_id]
    partial = {"COA-001": 6, "COA-002": 5, "COA-003": 5}[case_id]
    review = {
        "case_id": case_id,
        "schema_version": "0.1-alpha",
        "mapped_record_valid": True,  # set after validate
        "mapping_result": "PARTIAL",
        "exact_mapping_count": exact,
        "partial_mapping_count": partial,
        "not_representable_count": len(gaps),
        "gaps": gaps,
        "source_unavailable": False,
        "notes": "Seed hand-reviewed PARTIAL mapping; confirms issues #1–#4 as applicable.",
    }
    return source, record, review


def map_case(case_id: str, meta: dict, ext: dict | None, parsed: dict | None, fetch_ok: bool) -> tuple[dict, dict, str]:
    """Return record, review, mapping_result."""
    gaps: list[dict] = []
    exact = 0
    partial = 0
    ext = ext or {}
    parsed = parsed or empty_stub()

    batch = ext.get("batch_observed") or (parsed.get("meta") or {}).get("batch")
    sample = ext.get("sample_observed") or (parsed.get("meta") or {}).get("sample")
    if batch is not None and str(batch) != "":
        cultivation_batch_id = str(batch)
        exact += 1
    elif sample:
        cultivation_batch_id = str(sample)
        partial += 1
        gaps.append(gap("batch_id_missing_used_sample", "No batch id; used sample id", "IMPORTANT"))
    else:
        cultivation_batch_id = f"corpus-{case_id.lower()}-unknown-batch"
        partial += 1
        gaps.append(gap("batch_id_missing_placeholder", "No batch/sample id; deterministic placeholder for schema minLength", "IMPORTANT"))

    lab = ext.get("laboratory_verified_or_observed")
    client = ext.get("client_observed")
    product = meta.get("product_hint") or ext.get("title_verified")
    jcode = jurisdiction_code(meta.get("jurisdiction_hint"))

    record: dict[str, Any] = {
        "schema_version": "0.1-alpha",
        "record_id": f"corpus-{case_id.lower()}",
        "cultivation_batch_id": cultivation_batch_id,
        "created_at": CREATED_AT,
        "updated_at": CREATED_AT,
        "producer": {
            "organization_name": client or meta.get("source_group") or "unknown-producer",
            "jurisdiction": jcode,
        },
        "cultivar": {
            "reported_name": (str(product).split("(")[0].strip()[:120] if product else "unknown") or "unknown",
            "identity_status": "reported",
        },
        "lab_results": {
            "lab_name": lab,
            "sample_id": sample,
            "provenance": "laboratory_verified" if fetch_ok else "derived",
            "notes": f"Mapped from public COA corpus case {case_id}. WeedDAO does not independently re-verify laboratory measurements.",
        },
        "provenance": {
            "record": "derived",
            "lab_results": "laboratory_verified" if fetch_ok else "derived",
            "notes": "Public COA corpus mapping by WeedDAO Research. Not an external implementation claim.",
        },
        "extensions": {
            "weeddao_corpus": {
                "case_id": case_id,
                "source_url": meta["source_url"],
                "source_tier": meta["source_tier"],
                "source_group": meta.get("source_group"),
                "product_hint": meta.get("product_hint"),
                "product_type_hint": meta.get("product_type_hint"),
                "title_verified": ext.get("title_verified"),
                "overall_result_observed": ext.get("overall_result_observed"),
                "units_observed": ext.get("units_observed"),
                "panels_observed": ext.get("panels_observed"),
            }
        },
    }

    # Cannabinoids
    cann: dict[str, Any] = {}
    for key, entry in (parsed.get("cannabinoids") or {}).items():
        if key not in CANN_KEYS:
            continue
        if entry.get("kind") != "numeric" or entry.get("value") is None:
            continue
        unit = unit_to_schema(entry.get("unit") or "%")
        if unit is None:
            continue
        cann[key] = {"value": entry["value"], "unit": unit, "provenance": "laboratory_verified"}
        exact += 1
        if entry.get("alt"):
            record["extensions"]["weeddao_corpus"].setdefault("cannabinoids_alt_units", {})[key] = entry["alt"]
            parsed["multi_unit"] = True
    if cann:
        record["lab_results"]["cannabinoids"] = cann

    # Terpenes
    terps = []
    for t in parsed.get("terpenes") or []:
        if t.get("value") is None:
            continue
        unit = t.get("unit") or "%"
        if unit not in ("%", "mg/g", "ppm"):
            unit = "%"
        terps.append({"name": t["name"], "value": t["value"], "unit": unit})
        exact += 1
    if terps:
        record["lab_results"]["terpenes"] = terps
    if (parsed.get("meta") or {}).get("total_terpenes") is not None:
        record["lab_results"]["total_terpenes"] = {
            "value": parsed["meta"]["total_terpenes"],
            "unit": "%",
        }
        # total_terpenes may be additionalProperties on lab_results
        exact += 1

    # Safety panels
    safety: dict[str, Any] = {}
    panels = parsed.get("panels") or {}
    for pkey in ("microbials", "pesticides", "heavy_metals", "residual_solvents", "mycotoxins"):
        st = panels.get(pkey)
        if st in ("pass", "fail", "not_tested", "partial", "not_applicable"):
            safety[pkey] = {"status": st}
            exact += 1
    if safety:
        record["lab_results"]["safety"] = safety

    # Gaps from ND / below-limit / multi-unit / metadata
    if parsed.get("nd_cannabinoids") or parsed.get("nd_terpenes") or ext.get("uses_nd"):
        gaps.append(gap(
            "nd_not_representable",
            f"ND observed; omitted from core. examples={list(parsed.get('nd_cannabinoids') or [])[:8]}",
            "CRITICAL_INTEROPERABILITY", 3,
        ))
    if parsed.get("below_limit_cannabinoids") or parsed.get("below_limit_terpenes") or ext.get("uses_below_limit"):
        gaps.append(gap(
            "below_reporting_limit_qualifier",
            f"Below-limit qualifiers observed; omitted. examples={list(parsed.get('below_limit_cannabinoids') or [])[:8]}",
            "CRITICAL_INTEROPERABILITY", 1,
        ))
    units = ext.get("units_observed") or []
    multi = bool(parsed.get("multi_unit")) or len([u for u in units if any(x in str(u).lower() for x in ("%","mg/g","mg/serving","mg/ml","mg/unit"))]) >= 2
    if multi:
        gaps.append(gap(
            "multi_unit_cannabinoid",
            f"Concurrent multi-unit reporting; primary kept in core. units_observed={units}",
            "CRITICAL_INTEROPERABILITY", 4,
        ))
    if ext.get("uses_not_performed") or ext.get("uses_nt_or_not_tested"):
        gaps.append(gap("analyte_level_not_performed", "NOT TESTED / NOT PERFORMED on source", "CRITICAL_INTEROPERABILITY", 2))
    if ext.get("uses_nr_or_not_reported"):
        gaps.append(gap("not_reported", "NOT REPORTED on source", "IMPORTANT"))
    if ext.get("has_metrc_or_regulatory_tracking") or (parsed.get("meta") or {}).get("metrc_src"):
        gaps.append(gap("regulatory_tracking", "METRC/regulatory tracking present", "JURISDICTION_SPECIFIC"))
        if (parsed.get("meta") or {}).get("metrc_src"):
            record["extensions"]["weeddao_corpus"]["metrc_src_tag"] = parsed["meta"]["metrc_src"]
        if (parsed.get("meta") or {}).get("metrc_test"):
            record["extensions"]["weeddao_corpus"]["metrc_testing_tag"] = parsed["meta"]["metrc_test"]
        partial += 1
    if ext.get("has_sample_lifecycle_metadata"):
        gaps.append(gap("sample_lifecycle_metadata", "Collected/received lifecycle metadata on source", "IMPORTANT"))
    panels_obs = set(ext.get("panels_observed") or [])
    if "foreign_matter" in panels_obs or parsed.get("foreign_material"):
        gaps.append(gap("foreign_material", "Foreign material / visual inspection on source", "IMPORTANT"))
        record["extensions"]["weeddao_corpus"]["foreign_material"] = parsed.get("foreign_material") or "observed"
        partial += 1
    if "moisture" in panels_obs or parsed.get("moisture") is not None:
        gaps.append(gap("moisture_not_in_core", "Moisture on source; no first-class moisture object", "OPTIONAL"))
        if parsed.get("moisture") is not None:
            record["extensions"]["weeddao_corpus"]["moisture_percent"] = parsed["moisture"]
        partial += 1
    if "water_activity" in panels_obs or parsed.get("water_activity") is not None:
        gaps.append(gap("water_activity_not_in_core", "Water activity on source", "OPTIONAL"))
        if parsed.get("water_activity") is not None:
            record["extensions"]["weeddao_corpus"]["water_activity"] = parsed["water_activity"]
        partial += 1

    if not fetch_ok:
        gaps.append(gap("source_unavailable_or_unparsed", "SOURCE_UNAVAILABLE at fetch time or empty extract", "IMPORTANT"))
        record["extensions"]["weeddao_corpus"]["source_unavailable"] = True
        record["lab_results"]["notes"] += " SOURCE_UNAVAILABLE at corpus fetch time."

    if not cann and not terps and fetch_ok:
        gaps.append(gap("analyte_tables_unparsed", "Fetch succeeded but numeric analyte tables not reliably parsed; metadata-only mapping", "IMPORTANT"))

    important = {
        "nd_not_representable", "below_reporting_limit_qualifier", "multi_unit_cannabinoid",
        "analyte_level_not_performed", "source_unavailable_or_unparsed",
    }
    dropped_important = any(g["gap_key"] in important for g in gaps)
    has_numeric = bool(cann) or bool(terps)

    if dropped_important:
        mapping_result = "PARTIAL"
    elif has_numeric and not gaps:
        mapping_result = "FULL"
    elif has_numeric and all(g["severity"] in ("OPTIONAL", "JURISDICTION_SPECIFIC", "NICE_TO_HAVE") for g in gaps):
        mapping_result = "FULL"
    else:
        mapping_result = "PARTIAL"

    # Never FULL when important semantics dropped
    if dropped_important:
        mapping_result = "PARTIAL"

    review = {
        "case_id": case_id,
        "schema_version": "0.1-alpha",
        "mapped_record_valid": False,
        "mapping_result": mapping_result,
        "exact_mapping_count": exact,
        "partial_mapping_count": partial,
        "not_representable_count": len(gaps),
        "gaps": gaps,
        "source_unavailable": not fetch_ok,
        "notes": "Automated corpus mapping against frozen v0.1-alpha; numeric values only when parseable; no fabrication.",
    }
    return record, review, mapping_result


def empty_stub() -> dict:
    return {
        "cannabinoids": {}, "terpenes": [], "nd_cannabinoids": [], "below_limit_cannabinoids": [],
        "nd_terpenes": [], "below_limit_terpenes": [], "multi_unit": False, "meta": {},
        "panels": {}, "moisture": None, "water_activity": None, "foreign_material": None,
    }
