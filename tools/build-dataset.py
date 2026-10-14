#!/usr/bin/env python3
"""
Build the release artifact for the GERMLINE corpus: a deterministic, self-contained ZIP.

The same content always produces the same ZIP bytes (fixed timestamps, sorted
entries) so independent parties can verify builds against each other.

Output:
    dist/germline-corpus-v<version>.zip
        ├── README.md / DATASHEET.md / NOTICE.md / LICENSE-DATA / LICENSE / CITATION.cff
        ├── MANIFEST.sha256      (checksums of every packaged file)
        ├── BUILD.json           (provenance: commit, counts, build date)
        ├── corpus/**            (100 antibodies + ABX docs + indexes + logs)
        ├── schema/abx-0.1.schema.json
        ├── tools/abx.py
        └── docs/rfc/**
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
VERSION = "0.1.0"
PKG = f"germline-corpus-v{VERSION}"
STAMP = (2026, 10, 14, 0, 0, 0)  # fixed DOS timestamp -> reproducible archives


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit_date() -> str:
    """Deterministic build stamp: the source commit's own date (no wall clock)."""
    try:
        return subprocess.run(
            ["git", "show", "-s", "--format=%cI", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return "unknown"


def git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return "unknown"


def collect() -> list[tuple[str, Path]]:
    """(archive name, source path) — deterministic and explicit."""
    entries: list[tuple[str, Path]] = []

    def add(src: Path, arc: str) -> None:
        if src.is_file():
            entries.append((arc, src))
        elif src.is_dir():
            for p in sorted(src.rglob("*")):
                if p.is_file():
                    rel = p.relative_to(src).as_posix()
                    entries.append((f"{arc}/{rel}", p))

    # package-level documents
    entries += [
        ("README.md", ROOT / "dataset" / "README.md"),
        ("DATASHEET.md", ROOT / "dataset" / "DATASHEET.md"),
        ("NOTICE.md", ROOT / "dataset" / "NOTICE.md"),
        ("LICENSE-DATA", ROOT / "dataset" / "LICENSE-DATA"),
        ("LICENSE", ROOT / "LICENSE"),
        ("CITATION.cff", ROOT / "CITATION.cff"),
        ("metadata/zenodo-deposit.json", ROOT / "dataset" / "metadata" / "zenodo-deposit.json"),
    ]
    # content trees
    add(ROOT / "corpus", "corpus")
    entries.append(("schema/abx-0.1.schema.json", ROOT / "schema" / "abx-0.1.schema.json"))
    entries.append(("tools/abx.py", ROOT / "tools" / "abx.py"))
    add(ROOT / "docs" / "rfc", "docs/rfc")

    missing = [arc for arc, src in entries if not src.is_file()]
    if missing:
        raise SystemExit(f"missing sources: {missing}")
    return sorted(entries, key=lambda e: e[0])


def main() -> int:
    DIST.mkdir(exist_ok=True)
    entries = collect()

    # MANIFEST.sha256 (over sources), generated file — not recursive
    lines = [f"{sha256_file(src)}  {arc}" for arc, src in entries]
    manifest = "\n".join(lines) + "\n"

    stats = json.loads((ROOT / "corpus" / "stats.json").read_text(encoding="utf-8"))
    build = {
        "package": PKG,
        "version": VERSION,
        "built_at": git_commit_date(),  # deterministic: source commit date
        "source_commit": git_commit(),
        "generator": "tools/build-dataset.py",
        "counts": {
            "antibodies": stats["totals"]["antibodies"],
            "projects": stats["totals"]["projects"],
            "verified": stats["totals"].get("verified", 0),
            "abx_documents": sum(1 for a, _ in entries if a.startswith("corpus/abx/") and a.endswith(".abx.json")),
        },
        "policy": "fixed, publicly disclosed vulnerabilities only",
    }

    payload: list[tuple[str, bytes]] = [(arc, src.read_bytes()) for arc, src in entries]
    payload.append(("MANIFEST.sha256", manifest.encode()))
    payload.append(("BUILD.json", (json.dumps(build, ensure_ascii=False, indent=2) + "\n").encode()))
    payload.sort(key=lambda e: e[0])

    zip_path = DIST / f"{PKG}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for arc, data in payload:
            info = zipfile.ZipInfo(filename=f"{PKG}/{arc}", date_time=STAMP)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)

    (DIST / f"{PKG}.zip.sha256").write_text(f"{sha256_file(zip_path)}  {zip_path.name}\n", encoding="utf-8")

    print(f"✅ {zip_path} ({zip_path.stat().st_size/1024:.0f} KB, {len(payload)} files)")
    print(f"   sha256: {sha256_file(zip_path)}")
    print(f"   commit: {build['source_commit'][:12]} | antibodies: {build['counts']['antibodies']} "
          f"| verified: {build['counts']['verified']} | ABX docs: {build['counts']['abx_documents']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
