from __future__ import annotations

import copy
import json

from jsonschema import Draft202012Validator

from ci.validate_governance import ROOT, SCHEMA, validate


def test_candidate_governance_records_are_valid() -> None:
    assert validate() == []


def test_schema_rejects_unknown_fields() -> None:
    record = json.loads((ROOT / "governance/records/BFC-PROGRAMME-001.json").read_text())
    hostile = copy.deepcopy(record)
    hostile["may_promote_now"] = True
    assert list(Draft202012Validator(SCHEMA).iter_errors(hostile))


def test_schema_rejects_unsafe_subject_path() -> None:
    record = json.loads((ROOT / "governance/records/BFC-PROGRAMME-001.json").read_text())
    hostile = copy.deepcopy(record)
    hostile["subject"]["path"] = "../outside.json"
    assert list(Draft202012Validator(SCHEMA).iter_errors(hostile))
