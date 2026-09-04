from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


def indexed_bytes(root: Path, relative: str) -> bytes:
    """Return the canonical staged blob, independent of checkout line endings."""
    return subprocess.run(
        ["git", "show", f":{relative}"],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout


def main() -> None:
    root = Path(__file__).parents[1]
    records = []
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    for relative in sorted(line for line in result.stdout.splitlines() if line):
        if relative == "MANIFEST.json":
            continue
        path = root / relative
        if path.is_file():
            content = indexed_bytes(root, relative)
            records.append(
                {
                    "path": relative.replace("\\", "/"),
                    "bytes": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                }
            )
    output = root / "MANIFEST.json"
    output.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
