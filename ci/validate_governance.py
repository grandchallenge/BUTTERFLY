from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[1]
SCHEMA = json.loads((ROOT / "schemas/institutional_record.schema.json").read_text(encoding="utf-8"))
RECORDS = ROOT / "governance/records"
REQUIRED_CLASSES = {
    "programme", "work_package", "claim_ledger", "negative_knowledge", "promotion"
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate() -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(SCHEMA)
    records: list[dict[str, object]] = []
    for path in sorted(RECORDS.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        records.append(record)
        for error in validator.iter_errors(record):
            errors.append(f"{path.relative_to(ROOT)}: schema: {error.message}")
        subject = record.get("subject", {})
        if isinstance(subject, dict):
            relative = subject.get("path")
            expected = subject.get("sha256")
            if isinstance(relative, str) and expected not in {None, "PENDING_EXACT_CANDIDATE"}:
                target = ROOT / relative
                if not target.is_file() or digest(target) != expected:
                    errors.append(f"{path.relative_to(ROOT)}: subject digest mismatch")

    classes = {str(record.get("record_class")) for record in records}
    missing = REQUIRED_CLASSES - classes
    if missing:
        errors.append(f"missing record classes: {sorted(missing)}")

    admissions = [record for record in records if record.get("identifier") == "BFC-ADMISSION-001"]
    if len(admissions) != 1:
        errors.append("exactly one BFC-ADMISSION-001 record is required")
    else:
        admission = admissions[0]
        reviews = admission.get("reviews", [])
        roles = [review.get("role") for review in reviews if isinstance(review, dict)] if isinstance(reviews, list) else []
        if len(roles) != len(set(roles)):
            errors.append("BFC-ADMISSION-001 contains duplicate review roles")
        if admission.get("status") in {"admitted", "promoted"}:
            if admission.get("unresolved_obligations"):
                errors.append("admitted record retains unresolved obligations")
            if any(review.get("status") != "approved" for review in reviews if isinstance(review, dict)):
                errors.append("admitted record has a non-approved review")
            by_role = {review["role"]: review for review in reviews if isinstance(review, dict)}
            adversary = by_role.get("Adversary", {})
            referee = by_role.get("Referee", {})
            if adversary.get("reviewer") == referee.get("reviewer") or adversary.get("session") == referee.get("session"):
                errors.append("Adversary and Referee must have distinct reviewers and sessions")
    return errors


def main() -> int:
    errors = validate()
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
