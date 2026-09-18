#!/usr/bin/env python3
"""Canonical stats calculator for WeedDAO Public COA Corpus v0.1.
Re-reads cases+reviews+mappings and regenerates manifest + build_stats.json + docs counts.
Run after any corpus QA edit: python corpus/v0.1/scripts/recompute_stats.py
"""
from __future__ import annotations
import csv, hashlib, json, subprocess, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORPUS = ROOT / "corpus" / "v0.1"
CASES, MAPPINGS, REVIEWS = CORPUS/"cases", CORPUS/"mappings", CORPUS/"reviews"
DOCS = ROOT / "docs"
SCHEMA = ROOT / "schemas" / "weeddao-cultivation-record-v0.1-alpha.schema.json"
PIPELINE = {"analyte_tables_unparsed","source_unavailable_or_unparsed","batch_id_missing_placeholder"}
OPTIONAL = {"foreign_material","moisture_not_in_core","water_activity_not_in_core","best_by_date","homogeneity_not_in_core"}

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def dump(p, o):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(o, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def main():
    rows=[]; reviews=[]
    for i in range(1,51):
        cid=f"COA-{i:03d}"
        src=load(CASES/f"coa-{i:03d}-source.json")
        rev=load(REVIEWS/f"coa-{i:03d}-review.json")
        rec=load(MAPPINGS/f"coa-{i:03d}-weeddao-record.json")
        reviews.append(rev)
        panels=set(src.get("panels_observed") or [])
        units=src.get("units_observed") or []
        ext=(rec.get("extensions") or {}).get("weeddao_corpus") or {}
        contains_failure=bool(src.get("overall_status") and str(src["overall_status"]).upper()=="FAIL")
        if ext.get("contains_failure") or str(ext.get("batch_result") or "").upper()=="FAIL":
            contains_failure=True
        multi=len([u for u in units if any(x in str(u).lower() for x in ("%","mg/g","mg/serving","mg/ml","mg/unit","mg/package"))])>=2
        if any(g["gap_key"]=="multi_unit_cannabinoid" for g in rev.get("gaps") or []):
            multi=True
        rows.append({
            "case_id":cid,"source_url":src["source_url"],"source_tier":src["source_tier"],
            "retrieved_at":src.get("retrieved_at"),"jurisdiction":src.get("jurisdiction_hint"),
            "producer_or_brand":src.get("producer_or_brand"),"laboratory":src.get("laboratory"),
            "product_name":src.get("product_name"),"product_type":src.get("product_type"),
            "batch_or_lot_id":src.get("batch_or_lot_id"),"sample_id":src.get("sample_id"),
            "overall_status":src.get("overall_status"),"coa_date":None,"primary_unit_types":units,
            "has_cannabinoids":("cannabinoid" in panels) if panels else None,
            "has_terpenes":("terpene" in panels) if panels else None,
            "has_microbials":("microbial" in panels) if panels else None,
            "has_pesticides":("pesticide" in panels) if panels else None,
            "has_heavy_metals":("heavy_metal" in panels) if panels else None,
            "has_residual_solvents":("residual_solvent" in panels) if panels else None,
            "has_mycotoxins":("mycotoxin" in panels) if panels else None,
            "has_moisture":("moisture" in panels) if panels else None,
            "has_water_activity":("water_activity" in panels) if panels else None,
            "has_foreign_material":("foreign_matter" in panels) if panels else None,
            "has_regulatory_tracking":bool(src.get("has_regulatory_tracking")),
            "has_sample_lifecycle":bool(src.get("has_sample_lifecycle")),
            "uses_nd":bool(src.get("uses_nd")),"uses_below_limit":bool(src.get("uses_below_limit")),
            "uses_not_tested":bool(src.get("uses_not_tested") or src.get("uses_not_performed")),
            "uses_not_reported":bool(src.get("uses_not_reported")),"uses_multi_unit":multi,
            "contains_numeric_contaminant_detection":None,"contains_failure":contains_failure,
            "mapping_result":rev.get("mapping_result"),"notes":src.get("notes"),
        })
    dump(CORPUS/"manifest.json", rows)
    keys=list(rows[0].keys())
    with (CORPUS/"manifest.csv").open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for r in rows:
            w.writerow({k:(json.dumps(v) if isinstance(v,(list,dict)) else v) for k,v in r.items()})

    primary=sum(1 for r in rows if r["source_tier"]=="primary")
    secondary=sum(1 for r in rows if r["source_tier"]=="secondary")
    seed=sum(1 for r in rows if str(r["source_tier"]).startswith("seed"))
    full=sum(1 for r in reviews if r["mapping_result"]=="FULL")
    partial=sum(1 for r in reviews if r["mapping_result"]=="PARTIAL")
    failed=sum(1 for r in reviews if r["mapping_result"]=="FAILED")
    unavail=sum(1 for r in rows if (not str(r["source_tier"]).startswith("seed")) and (
        load(CASES/f"coa-{r['case_id'].split('-')[1]}-source.json").get("source_unavailable") is True
        or load(CASES/f"coa-{r['case_id'].split('-')[1]}-source.json").get("fetch_ok") is False))
    jurisdictions=sorted({r["jurisdiction"] for r in rows if r.get("jurisdiction")})
    labs=sorted({r["laboratory"] for r in rows if r.get("laboratory")})
    producers=sorted({r["producer_or_brand"] for r in rows if r.get("producer_or_brand")})
    ptypes=sorted({r["product_type"] for r in rows if r.get("product_type")})
    gap_cases=defaultdict(set); gap_labs=defaultdict(set); gap_jurs=defaultdict(set); gap_ptypes=defaultdict(set)
    gap_sev={}; gap_issue={}; man_by={r["case_id"]:r for r in rows}
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
        if k in PIPELINE: evidence_class="PIPELINE_LIMITATIONS"
        elif k in OPTIONAL: evidence_class="OPTIONAL_METADATA"
        elif k=="regulatory_tracking" or gap_sev.get(k)=="JURISDICTION_SPECIFIC": evidence_class="JURISDICTION_SPECIFIC"
        else: evidence_class=evidence
        gap_stats.append({"gap_key":k,"cases_count":n,"cases_percent":round(100.0*n/50,1),
            "independent_labs_count":len(labs_c),"jurisdictions_count":len(jurs_c),
            "product_types_count":len(gap_ptypes[k]),"severity":gap_sev.get(k),
            "existing_issue":gap_issue.get(k),"evidence_class":evidence_class,"case_ids":sorted(cases)})
    fail_ids=[r["case_id"] for r in rows if r.get("contains_failure")]
    fail_types={}
    for cid in fail_ids:
        rec=load(MAPPINGS/f"coa-{cid.split('-')[1]}-weeddao-record.json")
        ext=(rec.get("extensions") or {}).get("weeddao_corpus") or {}
        fail_types[cid]={
            "overall_batch_failure": str(ext.get("batch_result") or "").upper()=="FAIL",
            "failure_types": ext.get("failure_types") or [],
            "panel_results": ext.get("panel_results") or {},
            "contaminant_safety_fail": False,
            "potency_spec_fail": "potency_spec" in (ext.get("failure_types") or []),
            "homogeneity_fail": "homogeneity" in (ext.get("failure_types") or []),
        }
    occ={
        "ND": sum(1 for r in rows if r.get("uses_nd")),
        "below_limit": sum(1 for r in rows if r.get("uses_below_limit")),
        "NOT_TESTED_OR_NOT_PERFORMED": sum(1 for r in rows if r.get("uses_not_tested")),
        "NOT_REPORTED": sum(1 for r in rows if r.get("uses_not_reported")),
        "multi_unit": sum(1 for r in rows if r.get("uses_multi_unit")),
        "sample_lifecycle": sum(1 for r in rows if r.get("has_sample_lifecycle")),
        "regulatory_tracking": sum(1 for r in rows if r.get("has_regulatory_tracking")),
        "water_activity": sum(1 for r in rows if r.get("has_water_activity")),
        "moisture": sum(1 for r in rows if r.get("has_moisture")),
        "foreign_material": sum(1 for r in rows if r.get("has_foreign_material")),
        "FAIL": sum(1 for r in rows if r.get("contains_failure")),
    }
    stats={
        "TOTAL_CASES":50,"SEED_CASES":seed,"NEW_PUBLIC_CASES":47,
        "PRIMARY_SOURCE_CASES":primary,"SECONDARY_SOURCE_CASES":secondary,
        "JURISDICTIONS":jurisdictions,"LABORATORIES":labs,"PRODUCERS":producers,"PRODUCT_TYPES":ptypes,
        "FULL_MAPPINGS":full,"PARTIAL_MAPPINGS":partial,"FAILED_MAPPINGS":failed,
        "SOURCE_UNAVAILABLE":unavail,"gap_stats":gap_stats,"occurrences":occ,
        "ACTUAL_FAIL_CASES":len(fail_ids),"FAIL_CASE_IDS":fail_ids,"FAIL_TYPES":fail_types,
        "schema_sha256":hashlib.sha256(SCHEMA.read_bytes()).hexdigest(),
        "computed_at":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    dump(CORPUS/"build_stats.json", stats)
    print(json.dumps({k:stats[k] for k in ["TOTAL_CASES","PRIMARY_SOURCE_CASES","SECONDARY_SOURCE_CASES","SOURCE_UNAVAILABLE","ACTUAL_FAIL_CASES","FAIL_CASE_IDS","occurrences"]}, indent=2))
    print("issue_counts", {g["gap_key"]: g["cases_count"] for g in gap_stats if g.get("existing_issue") in (1,2,3,4)})

if __name__ == "__main__":
    main()
