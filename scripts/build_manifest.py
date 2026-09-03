# ABOUTME: Regenerates the repository SHA-256 manifest from tracked and candidate public files.
# ABOUTME: Excludes the manifest itself and files ignored by Git.
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"


def public_files(root: Path = ROOT) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    paths = [root / line for line in result.stdout.splitlines()]
    return sorted(
        path for path in paths if path != root / MANIFEST.name and path.is_file()
    )


def main() -> None:
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT)}"
        for path in public_files()
    ]
    MANIFEST.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
