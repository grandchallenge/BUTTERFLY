from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[1]
SCHEMA = json.loads((ROOT / "schemas/institutional_record.schema.json").read_text(encoding="utf-8"))
RECORDS = ROOT / "governance/records"
REQUIRED_CLASSES = {
    "programme", "work_package", "claim_ledger", "negative_knowledge", "promotion"
}
REQUIRED_REVIEW_ROLES = {
    "Axiomatist", "Cartographer", "Compiler", "Verifier", "Adversary",
    "Formalist", "Amanuensis", "Referee", "Human Steward",
}


def committed_digest(commit: str, relative: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return hashlib.sha256(result.stdout).hexdigest()


def semantic_errors(records: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
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
            subject = admission.get("subject", {})
            if not isinstance(subject, dict) or "PENDING_EXACT_CANDIDATE" in {
                subject.get("commit"), subject.get("sha256")
            }:
                errors.append("admitted record has unresolved subject identity")
            if not admission.get("evidence"):
                errors.append("admitted record has no evidence")
            if admission.get("unresolved_obligations"):
                errors.append("admitted record retains unresolved obligations")
            if set(roles) != REQUIRED_REVIEW_ROLES:
                errors.append("admitted record does not contain the complete required office set")
            if any(review.get("status") != "approved" for review in reviews if isinstance(review, dict)):
                errors.append("admitted record has a non-approved review")
            if any(
                not review.get("evidence")
                or review.get("reviewer") == "pending"
                or review.get("session") == "pending"
                for review in reviews if isinstance(review, dict)
            ):
                errors.append("admitted record has incomplete review identity or evidence")
            by_role = {review["role"]: review for review in reviews if isinstance(review, dict)}
            adversary = by_role.get("Adversary", {})
            referee = by_role.get("Referee", {})
            if adversary.get("reviewer") == referee.get("reviewer") or adversary.get("session") == referee.get("session"):
                errors.append("Adversary and Referee must have distinct reviewers and sessions")
    promoted = [
        record for record in records
        if record.get("status") == "promoted"
        or any(
            isinstance(claim, dict) and claim.get("status") == "promoted"
            for claim in record.get("claims", []) if isinstance(record.get("claims"), list)
        )
    ]
    if promoted and (not admissions or admissions[0].get("status") != "admitted"):
        errors.append("promotion requires an admitted BFC-ADMISSION-001 record")
    for record in promoted:
        subject = record.get("subject", {})
        reviews = record.get("reviews", [])
        by_role = {
            review.get("role"): review
            for review in reviews
            if isinstance(review, dict)
        } if isinstance(reviews, list) else {}
        if record.get("unresolved_obligations"):
            errors.append(f"{record.get('identifier')}: promoted record retains obligations")
        if not record.get("evidence"):
            errors.append(f"{record.get('identifier')}: promoted record has no exact evidence")
        if not isinstance(subject, dict) or "PENDING_EXACT_CANDIDATE" in {
            subject.get("commit"), subject.get("sha256")
        }:
            errors.append(f"{record.get('identifier')}: promoted record has unresolved identity")
        for role in ("Referee", "Human Steward"):
            review = by_role.get(role, {})
            if (
                review.get("status") != "approved"
                or not review.get("evidence")
                or review.get("reviewer") in {None, "pending"}
                or review.get("session") in {None, "pending"}
            ):
                errors.append(f"{record.get('identifier')}: promotion lacks exact {role} authorization")
        if by_role.get("Referee", {}).get("reviewer") == by_role.get("Human Steward", {}).get("reviewer"):
            errors.append(f"{record.get('identifier')}: Referee and Human Steward must be distinct")
    return errors


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
            commit = subject.get("commit")
            expected = subject.get("sha256")
            if (
                isinstance(relative, str)
                and isinstance(commit, str)
                and expected not in {None, "PENDING_EXACT_CANDIDATE"}
                and committed_digest(commit, relative) != expected
            ):
                errors.append(f"{path.relative_to(ROOT)}: subject digest mismatch")
    return errors + semantic_errors(records)


def main() -> int:
    errors = validate()
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
