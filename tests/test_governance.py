from __future__ import annotations

import copy
import json

from jsonschema import Draft202012Validator

from ci.validate_governance import ROOT, SCHEMA, semantic_errors, validate


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

    hostile["subject"]["path"] = "C:/outside.json"
    assert list(Draft202012Validator(SCHEMA).iter_errors(hostile))


def test_admission_fails_closed_without_all_offices_and_exact_evidence() -> None:
    admission = json.loads((ROOT / "governance/records/BFC-ADMISSION-001.json").read_text())
    hostile = copy.deepcopy(admission)
    hostile["status"] = "admitted"
    hostile["unresolved_obligations"] = []
    hostile["subject"]["commit"] = "PENDING_EXACT_CANDIDATE"
    hostile["subject"]["sha256"] = "PENDING_EXACT_CANDIDATE"
    hostile["reviews"] = [
        {
            "role": role,
            "reviewer": role.lower(),
            "session": f"session-{role.lower()}",
            "status": "approved",
            "evidence": "exact finding",
        }
        for role in ("Adversary", "Referee")
    ]
    errors = semantic_errors([hostile])
    assert any("unresolved subject identity" in error for error in errors)
    assert any("complete required office set" in error for error in errors)


def test_claim_promotion_requires_claim_specific_referee_and_steward_authority() -> None:
    admission = json.loads((ROOT / "governance/records/BFC-ADMISSION-001.json").read_text())
    admission["status"] = "admitted"
    admission["unresolved_obligations"] = []
    for review in admission["reviews"]:
        review.update(
            reviewer=review["role"].lower(),
            session=f"session-{review['role'].lower()}",
            status="approved",
            evidence="exact finding",
        )
    claims = json.loads((ROOT / "governance/records/BFC-CLAIMS-001.json").read_text())
    claims["status"] = "promoted"
    claims["claims"][0]["status"] = "promoted"
    claims["unresolved_obligations"] = []
    errors = semantic_errors([admission, claims])
    assert any("promotion lacks exact Referee authorization" in error for error in errors)
    assert any("promotion lacks exact Human Steward authorization" in error for error in errors)


def test_same_system_may_staff_distinct_adversary_and_referee_passes() -> None:
    admission = json.loads((ROOT / "governance/records/BFC-ADMISSION-001.json").read_text())
    admission["status"] = "admitted"
    admission["unresolved_obligations"] = []
    for review in admission["reviews"]:
        review.update(
            reviewer=("human-steward" if review["role"] == "Human Steward" else "codex-system"),
            session=f"logical-pass-{review['role'].lower().replace(' ', '-')}",
            status="approved",
            evidence="role-scoped exact-subject finding",
        )

    errors = semantic_errors([admission])
    assert not any("Adversary and Referee" in error for error in errors)


def test_durable_docs_state_streamlined_multi_role_contract() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    operating_model = (ROOT / "docs/STREAMLINED_ROLE_OPERATING_MODEL.md").read_text(
        encoding="utf-8"
    )

    assert "same Codex system" in agents
    assert "routine_bounded" in contributing
    assert "No identity multiplication" in operating_model
