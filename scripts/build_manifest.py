from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


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
            records.append(
                {
                    "path": relative.replace("\\", "/"),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    output = root / "MANIFEST.json"
    output.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
