"""Focused Cannlytics → WeedDAO v0.2-draft bridge tests."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from bridges.cannlytics_to_weeddao import convert_lab_result  # noqa: E402

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"jsonschema required: {e}")

SCHEMA = json.loads(
    (ROOT / "schemas" / "weeddao-record-v0.2-draft.schema.json").read_text(encoding="utf-8")
)
VALIDATOR = Draft202012Validator(SCHEMA)
FIXTURES = ROOT / "compat" / "cannlytics" / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def assert_valid(record: dict) -> None:
    errors = sorted(VALIDATOR.iter_errors(record), key=lambda e: list(e.path))
    assert not errors, "\n".join(f"{list(e.path)}: {e.message}" for e in errors)


def walk_result_states(obj, acc=None):
    if acc is None:
        acc = []
    if isinstance(obj, dict):
        if "result_state" in obj:
            acc.append(obj["result_state"])
        for v in obj.values():
            walk_result_states(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            walk_result_states(v, acc)
    return acc


class TestCannlyticsBridge(unittest.TestCase):
    def test_numeric_percent_cannabinoids(self):
        src = load_fixture("01-numeric-flower.json")
        rec, report = convert_lab_result(src)
        self.assertIsNotNone(rec)
        assert_valid(rec)
        thc = rec["lab_results"]["cannabinoids"]["thc"]
        self.assertEqual(thc["result_state"], "detected")
        self.assertEqual(thc["measurements"][0]["unit"], "%")
        self.assertAlmostEqual(thc["measurements"][0]["value"], 0.91)
        self.assertIn("thca", rec["lab_results"]["cannabinoids"])

    def test_terpenes_top_level(self):
        src = load_fixture("01-numeric-flower.json")
        rec, _ = convert_lab_result(src)
        names = {t["name"] for t in rec["lab_results"]["terpenes"]}
        self.assertIn("beta_myrcene", names)
        self.assertIn("d_limonene", names)
        self.assertEqual(rec["lab_results"]["total_terpenes"]["result_state"], "detected")

    def test_multi_unit_preserved(self):
        src = load_fixture("04-resultdetail-loq-multiunit.json")
        rec, report = convert_lab_result(src)
        assert_valid(rec)
        thca = rec["lab_results"]["cannabinoids"]["thca"]
        units = {m["unit"] for m in thca["measurements"]}
        self.assertIn("%", units)
        self.assertIn("mg/g", units)
        self.assertTrue(report["flags"]["MULTI_UNIT_PRESERVED"])

    def test_pass_fail_assessment_only(self):
        src = load_fixture("03-status-nt-pass-fail.json")
        rec, _ = convert_lab_result(src)
        assert_valid(rec)
        self.assertEqual(rec["lab_results"]["safety"]["pesticides"]["status"], "pass")
        self.assertEqual(rec["lab_results"]["safety"]["heavy_metals"]["status"], "fail")
        # analytes: pass/fail → assessment, ND → not_detected
        pest = rec["lab_results"]["safety"]["pesticides"]["analytes"]
        mycl = next(a for a in pest if a["name"] == "Myclobutanil")
        self.assertEqual(mycl["result_state"], "not_detected")
        self.assertEqual(mycl.get("assessment"), "pass")

    def test_nt_never_becomes_not_tested(self):
        src = load_fixture("03-status-nt-pass-fail.json")
        rec, report = convert_lab_result(src)
        assert_valid(rec)
        states = walk_result_states(rec)
        # analyte NT value must not become not_tested
        myc = rec["lab_results"]["safety"]["mycotoxins"]["analytes"]
        afl = next(a for a in myc if "flatoxin" in a["name"] or a["name"] == "Aflatoxin")
        self.assertEqual(afl["result_state"], "unknown")
        self.assertEqual(afl.get("reported_as"), "nt")
        self.assertTrue(report["flags"]["AMBIGUOUS_NT"])
        # panel nt omitted
        self.assertNotIn("status", rec["lab_results"]["safety"].get("microbials", {}))
        self.assertTrue(report["flags"]["PANEL_NT_AMBIGUOUS"])
        self.assertNotIn("not_tested", states)

    def test_explicit_nd(self):
        src = load_fixture("03-status-nt-pass-fail.json")
        rec, _ = convert_lab_result(src)
        pest = rec["lab_results"]["safety"]["pesticides"]["analytes"]
        mycl = next(a for a in pest if a["name"] == "Myclobutanil")
        self.assertEqual(mycl["result_state"], "not_detected")

    def test_null_without_nd_not_zero(self):
        src = load_fixture("02-null-cannabinoids.json")
        rec, report = convert_lab_result(src)
        assert_valid(rec)
        cans = rec.get("lab_results", {}).get("cannabinoids") or {}
        # null floats omitted — not present as 0 or ND
        for k in ("thc", "thca", "cbd", "total_thc"):
            if k in cans:
                ar = cans[k]
                self.assertNotEqual(ar.get("result_state"), "not_detected")
                for m in ar.get("measurements") or []:
                    self.assertNotEqual(m.get("value"), 0)
        self.assertTrue(report["flags"]["ND_UNRECOVERABLE"])

    def test_explicit_below_loq(self):
        src = load_fixture("04-resultdetail-loq-multiunit.json")
        rec, _ = convert_lab_result(src)
        other = rec["lab_results"]["cannabinoids"].get("other") or []
        cbdv = next(a for a in other if a["name"] in ("CBDV", "cbdv"))
        self.assertEqual(cbdv["result_state"], "below_reporting_limit")

    def test_loq_without_qualifier_ambiguous(self):
        src = load_fixture("04-resultdetail-loq-multiunit.json")
        rec, report = convert_lab_result(src)
        other = rec["lab_results"]["cannabinoids"].get("other") or []
        cbc = next(a for a in other if a["name"] in ("CBC", "cbc"))
        self.assertEqual(cbc["result_state"], "unknown")
        self.assertTrue(report["flags"]["BELOW_LIMIT_STATE_AMBIGUOUS"])
        limit_types = {lim["type"] for lim in cbc.get("limits") or []}
        self.assertIn("LOQ", limit_types)
        self.assertIn("LOD", limit_types)

    def test_generic_limit_type_ambiguous(self):
        src = load_fixture("03-status-nt-pass-fail.json")
        rec, report = convert_lab_result(src)
        metals = rec["lab_results"]["safety"]["heavy_metals"]["analytes"]
        lead = next(a for a in metals if a["name"] == "Lead")
        types = {lim["type"] for lim in lead.get("limits") or []}
        self.assertIn("other", types)
        self.assertTrue(report["flags"]["LIMIT_TYPE_AMBIGUOUS"])

    def test_metrc_identifiers(self):
        src = load_fixture("01-numeric-flower.json")
        rec, _ = convert_lab_result(src)
        schemes = {e["scheme"] for e in rec["subject"]["external_identifiers"]}
        self.assertIn("metrc.lab", schemes)
        self.assertIn("metrc.source", schemes)
        self.assertIn("metrc.tag", schemes)

    def test_finished_product_subject(self):
        src = load_fixture("03-status-nt-pass-fail.json")
        rec, report = convert_lab_result(src)
        self.assertEqual(rec["subject"]["subject_type"], "product_batch")
        self.assertFalse(report["flags"]["SUBJECT_TYPE_AMBIGUOUS"])

    def test_ambiguous_flower_subject(self):
        src = load_fixture("01-numeric-flower.json")
        rec, report = convert_lab_result(src)
        self.assertEqual(rec["subject"]["subject_type"], "other")
        self.assertTrue(report["flags"]["SUBJECT_TYPE_AMBIGUOUS"])
        self.assertNotEqual(rec["subject"]["subject_type"], "cultivation_batch")

    def test_strain_to_cultivar_not_product_name(self):
        src = load_fixture("01-numeric-flower.json")
        rec, _ = convert_lab_result(src)
        self.assertEqual(rec["cultivar"]["reported_name"], "Orange Zkittlez")
        self.assertEqual(rec["cultivar"]["identity_status"], "reported")
        self.assertEqual(rec["subject"]["name"], "Synthetic Orange Zkittlez Flower")
        # product_name must not appear as cultivar
        self.assertNotEqual(rec["cultivar"]["reported_name"], src["product_name"])

    def test_product_name_not_in_cultivar_when_no_strain(self):
        src = load_fixture("03-status-nt-pass-fail.json")
        rec, _ = convert_lab_result(src)
        self.assertNotIn("cultivar", rec)
        self.assertEqual(rec["subject"]["name"], src["product_name"])

    def test_dates_lifecycle(self):
        src = load_fixture("01-numeric-flower.json")
        rec, _ = convert_lab_result(src)
        sample = rec["lab_results"]["sample"]
        self.assertTrue(sample["collected_at"].startswith("2026-03-01"))
        self.assertTrue(sample["received_at"].startswith("2026-03-01"))
        self.assertTrue(sample["produced_at"].startswith("2026-02-20"))
        self.assertTrue(rec["lab_results"]["tested_at"].startswith("2026-03-02"))
        self.assertNotIn("reported_at", sample)
        # date_expires not silently best_by
        self.assertNotIn("best_by", rec["lab_results"])

    def test_date_expires_omitted(self):
        src = load_fixture("04-resultdetail-loq-multiunit.json")
        rec, report = convert_lab_result(src)
        self.assertNotIn("best_by", rec["lab_results"])
        self.assertIn("date_expires", " ".join(report["unmapped"]))

    def test_structurally_unmappable(self):
        src = load_fixture("05-unmappable-no-id.json")
        rec, report = convert_lab_result(src)
        self.assertIsNone(rec)
        self.assertTrue(report["flags"]["STRUCTURALLY_UNMAPPABLE"])
        self.assertEqual(report["flags"]["audit_class"], "STRUCTURALLY_UNMAPPABLE")

    def test_schema_validation_examples_pair(self):
        src = load_fixture("01-numeric-flower.json")
        rec, _ = convert_lab_result(src)
        assert_valid(rec)
        # overall_status not applied as panel
        self.assertEqual(
            rec.get("outcomes", {}).get("cannlytics_overall_status"),
            "pass",
        )

    def test_provenance_extension(self):
        src = load_fixture("01-numeric-flower.json")
        rec, _ = convert_lab_result(src)
        bridge = rec["extensions"]["cannlytics_bridge"]
        self.assertEqual(bridge["upstream_project"], "cannlytics/cannabis_results")
        self.assertEqual(
            bridge["upstream_schema_commit"],
            "a4e05a9f7367ac0b1637bd84773875b3bd1453ec",
        )
        self.assertEqual(bridge["upstream_record_id"], "synth-flower-001")
        self.assertIn("bridge_version", bridge)

    def test_cbd_zero_is_detected_not_null_coercion(self):
        """Present numeric 0.0 is a real measurement; null is different."""
        src = load_fixture("03-status-nt-pass-fail.json")
        rec, _ = convert_lab_result(src)
        cbd = rec["lab_results"]["cannabinoids"]["cbd"]
        self.assertEqual(cbd["result_state"], "detected")
        self.assertEqual(cbd["measurements"][0]["value"], 0.0)


if __name__ == "__main__":
    unittest.main()
