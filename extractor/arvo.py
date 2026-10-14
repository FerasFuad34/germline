#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERMLINE — Antibody Extractor v0.1

Turns the ARVO reproducible-vulnerability dataset (arvo.db, from OSS-Fuzz)
into a GERMLINE antibody corpus: portable, self-contained regression
"antibodies" — one folder per vulnerability.

Each generated antibody is a DRAFT: it must be double-checked on a Docker host
(fail on vulnerable image / pass on fixed image) before any "validated" claim.

Usage:
    python3 extractor/arvo.py --db arvo-workspace/arvo.db --out corpus \
        --selection extractor/selection.yaml [--dry-run] [--target 100]

Outputs:
    corpus/antibodies/AB-XXXXXX/{manifest.yaml, README.md, meta.json, double-check.sh}
    corpus/id-map.json      stable localId <-> AB-id mapping
    corpus/INDEX.md         human index
    corpus/stats.json       machine stats
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

# ───────────────────────────── crash type mapping ────────────────────────────

CWE_MAP = {
    "heap-buffer-overflow": ["CWE-122"],
    "stack-buffer-overflow": ["CWE-121"],
    "global-buffer-overflow": ["CWE-119"],
    "heap-use-after-free": ["CWE-416"],
    "use-after-free": ["CWE-416"],
    "double-free": ["CWE-415"],
    "use-of-uninitialized-value": ["CWE-457"],
    "null-dereference": ["CWE-476"],
    "signed-integer-overflow": ["CWE-190"],
    "unsigned-integer-overflow": ["CWE-190"],
    "integer-overflow": ["CWE-190"],
    "division-by-zero": ["CWE-369"],
    "out-of-memory": ["CWE-400"],
    "timeout": ["CWE-400"],
    "stack-overflow": ["CWE-674"],
    "assertion-failure": ["CWE-617"],
    "assert": ["CWE-617"],
    "segv": ["CWE-476"],
    "memcpy-param-overlap": ["CWE-119"],
    "negative-size-param": ["CWE-119"],
    "index-out-of-bounds": ["CWE-129"],
    "out-of-bounds": ["CWE-787"],
    "bad-free": ["CWE-590"],
    "heap-double-free": ["CWE-415"],
    "stack-use-after-return": ["CWE-562"],
    "stack-buffer-underflow": ["CWE-124"],
    "bad-cast": ["CWE-704"],
}

CLASS_RULES = [
    (("use-of-uninitialized-value", "uninitialized"), "memory-safety"),
    (("buffer-overflow", "use-after-free", "double-free", "segv", "memcpy", "negative-size",
      "index-out-of-bounds", "out-of-bounds", "unknown read", "unknown write"), "memory-safety"),
    (("integer-overflow", "division-by-zero"), "integer-overflow"),
    (("out-of-memory", "timeout", "stack-overflow"), "dos"),
    (("assert",), "logic"),
]

SANITIZER_MARKER = {
    "asan": "ERROR: AddressSanitizer",
    "msan": "WARNING: MemorySanitizer",
    "ubsan": "runtime error:",
}


ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
WS_RE = re.compile(r"[ \t]+")


def first_line(value: str) -> str:
    """ARVO stores multi-commit fixes and odd multi-line targets; keep scalars scalar."""
    return (value or "").splitlines()[0].strip() if value else ""


def strip_ansi(text: str) -> str:
    """Remove terminal escape sequences: manifests must stay portable, strict-parsable YAML."""
    text = ANSI_RE.sub("", text or "")
    return WS_RE.sub(" ", text).strip()


def normalize_crash_type(crash_type: str) -> str:
    """'Heap-buffer-overflow READ 4' -> 'heap-buffer-overflow' (drop ACCESS size suffixes)."""
    parts = (crash_type or "").strip().split()
    keep = []
    for p in parts:
        if p.upper() in ("READ", "WRITE", "{*}"):
            break
        if p.isdigit():
            break
        keep.append(p)
    return " ".join(keep).lower() or (crash_type or "").lower()


def crash_class(crash_type: str) -> str:
    low = normalize_crash_type(crash_type)
    for keys, cls in CLASS_RULES:
        if any(k in low for k in keys):
            return cls
    return "memory-safety"


def crash_cwes(crash_type: str) -> list[str]:
    return CWE_MAP.get(normalize_crash_type(crash_type), [])



def marker_for(sanitizer: str, crash_type: str, crash_output: str) -> str:
    """Prefer the canonical sanitizer banner; verify it appears in crash_output.

    Markers are normalized (ANSI stripped, whitespace collapsed, 120-char cap) so
    that generated manifests remain valid, portable YAML for any strict parser.
    """
    banner = SANITIZER_MARKER.get(sanitizer, "")
    if banner and banner in (crash_output or ""):
        return strip_ansi(banner)[:120]
    # fallback: first sanitizer-ish line found in output
    for line in (crash_output or "").splitlines():
        if "Sanitizer" in line or "runtime error:" in line:
            cleaned = strip_ansi(line)
            if cleaned:
                return cleaned[:120]
    return crash_type or "crash"


# ─────────────────────────────── selection ───────────────────────────────────

def read_selection(path: Path) -> dict:
    """Minimal YAML reader for our fixed-shape config (no external deps)."""
    sel = {"target": 100, "cap_per_crash_type": 2, "projects": {}, "fallbacks": []}
    section = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" "):
            if line.startswith("projects:"):
                section = "projects"
                continue
            if line.startswith("fallbacks:"):
                section = "fallbacks"
                rest = line.split(":", 1)[1].strip()
                if rest.startswith("["):
                    sel["fallbacks"] = [x.strip() for x in rest.strip("[]").split(",") if x.strip()]
                continue
            section = None
            if ":" in line:
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                if k in ("target", "cap_per_crash_type") and v.isdigit():
                    sel[k] = int(v)
            continue
        if section == "projects" and ":" in line:
            k, v = line.split(":", 1)
            if v.strip().isdigit():
                sel["projects"][k.strip()] = int(v.strip())
        elif section == "fallbacks" and line.strip().startswith("- "):
            sel["fallbacks"].append(line.strip()[2:].strip())
    return sel


def load_verification_state(corpus_dir: Path) -> dict:
    """Verification results are inputs to generation, so write-back stays deterministic."""
    path = corpus_dir / "verification-state.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"runs": []}


def pick_rows(cur, projects: dict[str, int], cap: int, target: int, fallbacks: list[str]) -> list[dict]:
    chosen, seen_ids = [], set()

    def take(project: str, quota: int) -> None:
        per_type: dict[str, int] = {}
        rows = cur.execute(
            "SELECT * FROM arvo WHERE reproduced=1 AND project=? ORDER BY localId ASC", (project,)
        ).fetchall()
        cols = [d[0] for d in cur.description]
        for row in rows:
            if quota <= 0:
                break
            rec = dict(zip(cols, row))
            ct = (rec.get("crash_type") or "").lower()
            if per_type.get(ct, 0) >= cap:
                continue
            if rec["localId"] in seen_ids:
                continue
            per_type[ct] = per_type.get(ct, 0) + 1
            seen_ids.add(rec["localId"])
            chosen.append(rec)
            quota -= 1

    for project, quota in projects.items():
        take(project, quota)

    # fill from fallbacks if short
    if len(chosen) < target:
        for project in fallbacks:
            if len(chosen) >= target:
                break
            take(project, target - len(chosen))

    return chosen[:target]


# ─────────────────────────────── generators ──────────────────────────────────

MANIFEST_TMPL = """\
# GERMLINE antibody — DRAFT (run tools/run-corpus-checks.sh to validate)
id: {ab_id}
title: {title_yaml}
cve: {cve}
cwe: {cwe}

origin:
  project: {project}
  generation: g0
  upstream: "OSS-Fuzz / ARVO (localId {local_id})"
  fixed_in: {fix_commit_short}

attack:
  class: {klass}
  target_fn: {fuzz_target_yaml}
  sanitizer: {sanitizer}
  crash_type: {crash_type_yaml}

test:
  kind: proof-of-vulnerability
  harness: "{run_vul}"
  expectation:
    on_vulnerable: crash
    on_fixed: clean
  detection_marker: {marker_yaml}

severity:
  level: {severity}

provenance:
  generated_by: "germline extractor v0.1 (ARVO {db_version})"
  verified_by: {verified_by}
  source:
    dataset: "ARVO — Atlas of Reproducible Vulnerabilities (EuroS&P 2026)"
    report: {report_url_yaml}
    repo: {repo_addr_yaml}
    fix_commit: {fix_commit_yaml}
    patch_url: {patch_url_yaml}
    docker:
      vulnerable: "{img_vul}"
      fixed: "{img_fix}"
  evidence:
    expected_crash_sha256: "{crash_sha}"
    expected_crash_excerpt_bytes: {excerpt_len}

status: {status}
"""

README_TMPL = """\
# {ab_id} — {title}

{status_line}

| | |
|---|---|
| Project | `{project}` |
| Class / CWE | `{klass}` / {cwe_display} |
| Sanitizer | `{sanitizer}` |
| Crash type | `{crash_type}` |
| Severity | {severity} |
| Fixed in | [{fix_commit_short}]({patch_url}) |
| Upstream report | {report_url} |
| Dataset | ARVO localId `{local_id}` |

## What this antibody guards

This is the historical vulnerability **{crash_type}** in `{project}`
(fuzz target: `{fuzz_target}`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   {marker}
{run_vul}

# Fixed build — expected to run clean:
{run_fix}
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`{marker}` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
"""

DOUBLECHECK_TMPL = """\
#!/usr/bin/env bash
# {ab_id} — double-check: fail on vulnerable / pass on fixed.
exec bash "$(cd "$(dirname "$0")/../../.." && pwd)/tools/double-check-one.sh" "{ab_id}" "$@"
"""


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="GERMLINE antibody extractor (ARVO → corpus)")
    ap.add_argument("--db", required=True, help="path to arvo.db")
    ap.add_argument("--out", required=True, help="corpus output directory")
    ap.add_argument("--selection", required=True, help="selection yaml")
    ap.add_argument("--target", type=int, default=None, help="override target count")
    ap.add_argument("--dry-run", action="store_true", help="print plan only")
    args = ap.parse_args()

    sel = read_selection(Path(args.selection))
    target = args.target or sel["target"]

    con = sqlite3.connect(args.db)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    db_version = "v3.0.0"
    rows = pick_rows(con.cursor(), sel["projects"], sel["cap_per_crash_type"], target, sel["fallbacks"])

    print(f"🧬 Selected {len(rows)} vulnerabilities (target {target})")
    if args.dry_run:
        for r in rows[:20]:
            print(f"  {r['project']:<16} {r['sanitizer']:<6} {r['crash_type']}")
        print(f"  ... ({len(rows)} total)")
        return 0

    out = Path(args.out)
    ab_dir = out / "antibodies"
    ab_dir.mkdir(parents=True, exist_ok=True)

    # verification write-back: statuses come from corpus/verification-state.json
    vstate = load_verification_state(out)
    vindex: dict[str, list[str]] = {}
    for run in vstate.get("runs", []):
        for res in run.get("results", []):
            if res.get("verdict") == "verified":
                vindex.setdefault(res["id"], []).append(
                    f"{run.get('runner', 'unknown')}:run-{run.get('run_id', '?')}@{run.get('date', '?')}"
                )

    # stable id map + per-antibody creation stamps (kept forever: ABX stability)
    idmeta_path = out / "id-meta.json"
    idmeta = json.loads(idmeta_path.read_text(encoding="utf-8")) if idmeta_path.exists() else {}

    # stable id map
    idmap_path = out / "id-map.json"
    idmap = json.loads(idmap_path.read_text(encoding="utf-8")) if idmap_path.exists() else {}
    next_num = max([int(v.split("-")[1]) for v in idmap.values()], default=0) + 1

    index_rows, stats = [], {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "source": {"dataset": "ARVO", "db_version": db_version, "table": "arvo"},
        "status": "draft — not yet double-checked",
        "totals": {"antibodies": 0, "projects": 0},
        "by_project": {}, "by_sanitizer": {}, "by_class": {}, "by_severity": {},
    }

    for rec in rows:
        local_id = rec["localId"]
        if str(local_id) in idmap:
            ab_id = idmap[str(local_id)]
        else:
            ab_id = f"AB-{next_num:06d}"
            idmap[str(local_id)] = ab_id
            next_num += 1

        idmeta.setdefault(ab_id, {"first_generated": stats["generated_at"], "arvo_local_id": local_id})

        project = rec["project"]
        sanitizer = rec["sanitizer"] or "unknown"
        crash_type = rec["crash_type"] or "unknown"
        severity = rec["severity"] or "unknown"
        fuzz_target = first_line(rec["fuzz_target"]) or "n/a"
        fix_commits = [c.strip() for c in (rec["fix_commit"] or "").splitlines() if c.strip()]
        fix_commit = fix_commits[0] if fix_commits else ""
        patch_url = first_line(rec["patch_url"])
        report_url = first_line(rec["report"]) or f"https://issues.oss-fuzz.com/issues/{local_id}"
        repo_addr = first_line(rec["repo_addr"])
        crash_out = rec["crash_output"] or ""
        run_vul = (rec["reproducer_vul"] or f"docker run --rm n132/arvo:{local_id}-vul arvo").replace(" -it ", " ")
        run_fix = (rec["reproducer_fix"] or f"docker run --rm n132/arvo:{local_id}-fix arvo").replace(" -it ", " ")

        klass = crash_class(crash_type)
        cwes = crash_cwes(crash_type)
        marker = marker_for(sanitizer, crash_type, crash_out)
        verified_by = vindex.get(ab_id, [])
        status = "validated" if verified_by else "draft"
        status_line = (
            "**Status: \U0001F7E2 VALIDATED** \u2014 double-checked on a real runner: crashes on the "
            "vulnerable build, stays clean on the fixed build (see `../../VERIFICATION.md`)."
            if status == "validated" else
            "**Status: \U0001F7E1 DRAFT** \u2014 generated from ARVO metadata; not yet double-checked on a Docker host."
        )
        title = f"{project}: {crash_type} in {fuzz_target}"[:180]
        crash_sha = sha256_hex(crash_out.encode("utf-8", "replace"))

        d = ab_dir / ab_id
        d.mkdir(exist_ok=True)

        (d / "manifest.yaml").write_text(MANIFEST_TMPL.format(
            ab_id=ab_id, title=title, cve="[]", cwe=json.dumps(cwes),
            project=project, local_id=local_id, fix_commit_short=fix_commit[:12],
            klass=klass, fuzz_target=fuzz_target, sanitizer=sanitizer, crash_type=crash_type,
            run_vul=run_vul, marker=marker, severity=severity,
            title_yaml=json.dumps(title), fuzz_target_yaml=json.dumps(fuzz_target),
            crash_type_yaml=json.dumps(crash_type), marker_yaml=json.dumps(marker),
            report_url_yaml=json.dumps(report_url), repo_addr_yaml=json.dumps(repo_addr),
            fix_commit_yaml=json.dumps(fix_commit), patch_url_yaml=json.dumps(patch_url),
            db_version=db_version, report_url=report_url, repo_addr=repo_addr,
            fix_commit=fix_commit, patch_url=patch_url,
            img_vul=f"n132/arvo:{local_id}-vul", img_fix=f"n132/arvo:{local_id}-fix",
            crash_sha=crash_sha, excerpt_len=min(2000, len(crash_out)),
            status=status, verified_by=json.dumps(verified_by),
        ), encoding="utf-8")

        (d / "README.md").write_text(README_TMPL.format(
            ab_id=ab_id, title=title, project=project, klass=klass,
            cwe_display=", ".join(cwes) if cwes else "—",
            sanitizer=sanitizer, crash_type=crash_type, severity=severity,
            fix_commit_short=fix_commit[:12], patch_url=patch_url,
            report_url=report_url, local_id=local_id, fuzz_target=fuzz_target,
            marker=marker, run_vul=run_vul, run_fix=run_fix, status_line=status_line,
        ), encoding="utf-8")

        (d / "meta.json").write_text(json.dumps({
            "id": ab_id, "arvo_local_id": local_id, "project": project,
            "sanitizer": sanitizer, "crash_type": crash_type, "severity": severity,
            "fuzz_target": fuzz_target, "fuzz_engine": rec["fuzz_engine"],
            "language": rec["language"], "repo": repo_addr, "fix_commit": fix_commit,
            "fix_commits": fix_commits,
            "patch_url": patch_url, "report_url": report_url,
            "docker": {"vulnerable": f"n132/arvo:{local_id}-vul", "fixed": f"n132/arvo:{local_id}-fix"},
            "detection_marker": marker,
            "expected_crash_sha256": crash_sha,
            "expected_crash_excerpt": crash_out[:2000],
            "expected_crash_excerpt_truncated": len(crash_out) > 2000,
            "generated_by": f"germline-extractor/0.1 (ARVO {db_version})",
        }, ensure_ascii=False, indent=2), encoding="utf-8")

        dc = d / "double-check.sh"
        dc.write_text(DOUBLECHECK_TMPL.format(ab_id=ab_id), encoding="utf-8")
        dc.chmod(0o755)

        index_rows.append({
            "id": ab_id, "project": project, "sanitizer": sanitizer,
            "crash_type": crash_type, "severity": severity,
            "fix_commit": fix_commit[:12], "report_url": report_url,
            "status": status,
        })
        stats["by_project"][project] = stats["by_project"].get(project, 0) + 1
        stats["by_sanitizer"][sanitizer] = stats["by_sanitizer"].get(sanitizer, 0) + 1
        stats["by_class"][klass] = stats["by_class"].get(klass, 0) + 1
        stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1

    validated_count = sum(1 for r in index_rows if r["status"] == "validated")
    stats["totals"]["antibodies"] = len(index_rows)
    stats["totals"]["projects"] = len(stats["by_project"])
    stats["totals"]["high_severity"] = stats["by_severity"].get("High", 0)
    stats["totals"]["verified"] = validated_count
    latest_run = vstate["runs"][-1].get("run_id") if vstate.get("runs") else None
    stats["status"] = (
        f"{validated_count} verified / {len(index_rows) - validated_count} draft — "
        f"double-check operational (latest run {latest_run})"
        if validated_count else "draft — not yet double-checked"
    )

    idmap_path.write_text(json.dumps(idmap, indent=2, sort_keys=True), encoding="utf-8")
    idmeta_path.write_text(json.dumps(idmeta, indent=2, sort_keys=True), encoding="utf-8")
    (out / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    # INDEX.md grouped by project
    lines = [
        "# GERMLINE Antibody Corpus — INDEX", "",
        f"**{len(index_rows)} antibodies** across **{len(stats['by_project'])} projects** — "
        f"generated {stats['generated_at']} from ARVO {db_version}.", "",
        f"> Status: \U0001F7E2 {validated_count} validated (double-checked on a real runner) \u00b7 "
        f"\U0001F7E1 {len(index_rows) - validated_count} draft \u2014 full run log in `VERIFICATION.md`.", "",
    ]
    by_proj: dict[str, list[dict]] = {}
    for r in index_rows:
        by_proj.setdefault(r["project"], []).append(r)
    for project, items in sorted(by_proj.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines += [f"## {project} ({len(items)})", "",
                  "| Antibody | Sanitizer | Crash type | Severity | Fix | Report |",
                  "|---|---|---|---|---|---|"]
        for r in items:
            icon = "\U0001F7E2" if r["status"] == "validated" else "\U0001F7E1"
            lines.append(
                f"| {icon} `{r['id']}` | {r['sanitizer']} | {r['crash_type']} | {r['severity']} "
                f"| `{r['fix_commit']}` | [link]({r['report_url']}) |"
            )
        lines.append("")
    (out / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"✅ Corpus written to {out}")
    print(f"   antibodies: {stats['totals']['antibodies']} | projects: {stats['totals']['projects']}")
    print(f"   verified: {validated_count} | draft: {len(index_rows) - validated_count}")
    print(f"   by sanitizer: {stats['by_sanitizer']}")
    print(f"   index: {out/'INDEX.md'} | stats: {out/'stats.json'} | id-map: {idmap_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
