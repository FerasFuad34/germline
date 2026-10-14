#!/usr/bin/env python3
"""
ABX reference implementation — RFC-0 (docs/rfc/0001-abx-antibody-exchange-format.md)

Subcommands
    convert   Render corpus manifests (authoring format) into ABX wire documents.
    validate  Level 1 (schema) / Level 2 (schema + invariants) / Level 3 (+ verified run).
    digest    Recompute and verify the integrity digest of a document.

Design notes
    * Deterministic: same inputs -> byte-identical outputs (canonical JSON, sorted keys).
    * Strict: unknown fields are rejected by the schema; invariants are enforced in code.
    * No execution: this tool never runs an antibody; that is the double-check's job.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML required for convert (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2)

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_SCHEMA = REPO_ROOT / "schema" / "abx-0.1.schema.json"

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
WS_RE = re.compile(r"[ \t]+")
ABX_VERSION = "0.1"
GENERATOR = "germline-extractor/0.1"
LICENSE = "Apache-2.0 (document) / CC-BY-4.0 (upstream data)"

ALLOWED_CLASSES = {
    "memory-safety", "injection", "auth-bypass", "integer-overflow", "logic",
    "info-disclosure", "dos", "supply-chain", "unknown",
}
ALLOWED_SANITIZERS = {"asan", "msan", "ubsan", "tsan", "none", "unknown"}
ALLOWED_SEVERITIES = {"Low", "Medium", "High", "Critical", "unknown"}
REGEX_DETECTORS = {"stdout-regex", "stderr-regex"}


# --------------------------------------------------------------------------- #
# canonicalization / digests
# --------------------------------------------------------------------------- #

def canonical_bytes(doc: dict) -> bytes:
    """Canonical JSON of the document *body* (integrity + signatures removed).

    Restricted RFC 8785 profile: sorted keys, no insignificant whitespace, UTF-8.
    """
    body = {k: v for k, v in doc.items() if k not in ("integrity", "signatures")}
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def body_digest(doc: dict) -> str:
    return hashlib.sha256(canonical_bytes(doc)).hexdigest()


def render(doc: dict) -> str:
    """Human-reviewable, deterministic on-disk rendering."""
    return json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def clean_excerpt(text: str, limit: int = 512) -> str:
    text = ANSI_RE.sub("", text or "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(WS_RE.sub(" ", line).strip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text[:limit]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_verification_state(corpus: Path) -> dict:
    state_path = corpus / "verification-state.json"
    if state_path.exists():
        return load_json(state_path)
    return {"runs": []}


def verified_index(state: dict) -> dict:
    """id -> list of ABX run objects (from multiple runs, append-only)."""
    out: dict[str, list] = {}
    for run in state.get("runs", []):
        for res in run.get("results", []):
            if res.get("verdict") != "verified":
                continue
            out.setdefault(res["id"], []).append({
                "runner": run.get("runner", "unknown"),
                "run_id": str(run.get("run_id", "")),
                "run_url": run.get("url", ""),
                "date": run.get("date", ""),
                "observed": {
                    "vulnerable": res.get("vulnerable", "crash"),
                    "fixed": res.get("fixed", "clean"),
                },
                "verdict": "verified",
            })
    return out


def detector_for(manifest: dict) -> dict:
    marker = str(manifest.get("test", {}).get("detection_marker", "")).strip()
    if marker.lower().startswith("exit-code"):
        digits = re.sub(r"[^0-9-]", "", marker)
        return {"type": "exit-code", "match": int(digits or "1")}
    if "sanitizer" in marker.lower():
        return {"type": "sanitizer-report", "match": marker}
    return {"type": "stdout-regex", "match": marker}


def sanitize_enum(value, allowed, fallback="unknown"):
    return value if value in allowed else fallback


# --------------------------------------------------------------------------- #
# convert
# --------------------------------------------------------------------------- #

def build_document(ab_dir: Path, stats: dict, verified: dict, idmeta: dict | None = None) -> dict:
    manifest = yaml.safe_load((ab_dir / "manifest.yaml").read_text(encoding="utf-8"))
    meta = load_json(ab_dir / "meta.json")
    ab_id = manifest["id"]

    origin = manifest.get("origin", {})
    vuln = manifest.get("attack", {})
    test = manifest.get("test", {})

    status = "validated" if ab_id in verified else "draft"

    doc = {
        "abx_version": ABX_VERSION,
        "kind": "antibody",
        "id": ab_id,
        "title": manifest["title"][:180],
        "subject": {
            "project": origin.get("project", "unknown"),
            "upstream": meta.get("repo") or "https://github.com/n132/ARVO-Meta",
            "language": meta.get("language", "unknown"),
            "generation": origin.get("generation", "g0"),
            "fixed_in": (meta.get("fix_commit") or "unknown")[:12],
        },
        "vulnerability": {
            "identifiers": {
                "cve": list(manifest.get("cve") or []),
                "cwe": list(manifest.get("cwe") or []),
                "oss_fuzz": str(meta["arvo_local_id"]),
            },
            "class": sanitize_enum(vuln.get("class"), ALLOWED_CLASSES),
            "crash_type": meta.get("crash_type") or "unknown",
            "sanitizer": sanitize_enum(meta.get("sanitizer"), ALLOWED_SANITIZERS),
            "severity": sanitize_enum(meta.get("severity"), ALLOWED_SEVERITIES),
            "cvss": None,
        },
        "challenge": {
            "kind": test.get("kind", "proof-of-vulnerability"),
            "harness": test.get("harness", ""),
            "target": meta.get("fuzz_target") or "n/a",
            "expect": {
                "vulnerable": test.get("expectation", {}).get("on_vulnerable", "crash"),
                "fixed": "clean",
            },
            "detector": detector_for(manifest),
        },
        "environments": {
            "vulnerable": {"type": "oci-image", "ref": meta["docker"]["vulnerable"]},
            "fixed": {"type": "oci-image", "ref": meta["docker"]["fixed"]},
        },
        "evidence": {
            "report": meta.get("report_url") or f"https://issues.oss-fuzz.com/issues/{meta['arvo_local_id']}",
            "patch": meta.get("patch_url") or meta.get("repo") or "https://github.com/n132/ARVO-Meta",
            "fix_commit": meta.get("fix_commit") or "unknown",
            "crash_digest": {"alg": "sha256", "value": meta["expected_crash_sha256"]},
            "crash_excerpt": clean_excerpt(meta.get("expected_crash_excerpt", "")),
        },
        "provenance": {
            "source": {
                "dataset": stats.get("source", {}).get("dataset", "ARVO"),
                "version": stats.get("source", {}).get("db_version", "unknown"),
                "record": str(meta["arvo_local_id"]),
            },
            "generated_by": GENERATOR,
            "generated_at": (idmeta or {}).get(ab_id, {}).get(
                "first_generated",
                stats.get("generated_at", datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")),
            ),
            "license": LICENSE,
        },
        "status": status,
    }

    if status == "validated":
        doc["verification"] = {"last_verdict": "verified", "runs": verified[ab_id]}

    # multi-commit fixes are real (394 ARVO records): carry the full list, keep the scalar as the first
    fix_commits = meta.get("fix_commits") or ([meta["fix_commit"]] if meta.get("fix_commit") else [])
    if len(fix_commits) > 1:
        doc["ext"] = {"sh.germline.fix_commits": fix_commits}

    doc["integrity"] = {"algorithm": "sha256", "value": body_digest(doc)}
    return doc


def cmd_convert(args) -> int:
    corpus = Path(args.corpus)
    out = Path(args.out)
    stats = load_json(corpus / "stats.json")
    verified = verified_index(load_verification_state(corpus))
    idmeta_path = corpus / "id-meta.json"
    idmeta = load_json(idmeta_path) if idmeta_path.exists() else {}

    ab_dirs = sorted((corpus / "antibodies").glob("AB-*"))
    if args.only:
        wanted = set(args.only)
        ab_dirs = [d for d in ab_dirs if d.name in wanted]
    if not ab_dirs:
        print("ERROR: no antibodies found", file=sys.stderr)
        return 2

    out.mkdir(parents=True, exist_ok=True)
    written = drift = 0
    for ab_dir in ab_dirs:
        doc = build_document(ab_dir, stats, verified, idmeta)
        target = out / f"{doc['id']}.abx.json"
        payload = render(doc)
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != payload:
                print(f"✗ drift: {target.name}")
                drift += 1
            continue
        target.write_text(payload, encoding="utf-8")
        written += 1

    if args.check:
        if drift:
            print(f"FAIL: {drift}/{len(ab_dirs)} documents differ from their sources", file=sys.stderr)
            return 1
        print(f"OK: {len(ab_dirs)} documents are in sync with the corpus")
        return 0

    validated = sum(1 for d in ab_dirs if d.name in verified)
    print(f"🧬 Rendered {written} ABX documents → {out}")
    print(f"   status: {validated} validated · {written - validated} draft")
    return 0


# --------------------------------------------------------------------------- #
# validate
# --------------------------------------------------------------------------- #

def check_invariants(doc: dict, seen_ids: dict) -> list[str]:
    errs: list[str] = []
    ab_id = doc.get("id", "?")

    # INV-1 — discrimination
    exp = doc.get("challenge", {}).get("expect", {})
    if exp.get("vulnerable") == exp.get("fixed"):
        errs.append("INV-1: expected observations on vulnerable/fixed sides are identical")

    # INV-2 — unique ids
    if ab_id in seen_ids:
        errs.append(f"INV-2: duplicate id (also in {seen_ids[ab_id]})")
    else:
        seen_ids[ab_id] = doc.get("title", "")[:40]

    # INV-3 — pinned environments
    for side in ("vulnerable", "fixed"):
        env = doc.get("environments", {}).get(side, {})
        ref = str(env.get("ref", ""))
        if not ref or ":" not in ref and env.get("type") == "oci-image":
            errs.append(f"INV-3: environment '{side}' lacks a pinned tag/digest")
        elif ref.endswith(":latest"):
            errs.append(f"INV-3: environment '{side}' uses a floating ':latest' tag")

    # INV-5 / INV-6 — verification semantics
    status = doc.get("status")
    runs = doc.get("verification", {}).get("runs", []) if "verification" in doc else []
    has_verified = any(r.get("verdict") == "verified" for r in runs)
    if status == "validated" and not has_verified:
        errs.append("INV-6: status 'validated' without any verified run")
    if status == "draft" and has_verified:
        errs.append("INV-6: a verified run exists but the document is still 'draft' (promote it)")
    if status == "validated" and doc.get("verification", {}).get("last_verdict") != "verified":
        errs.append("INV-5/6: last_verdict is not 'verified' while status is 'validated'")

    # INV-8 — positive detectors
    det = doc.get("challenge", {}).get("detector", {})
    if det.get("type") in REGEX_DETECTORS:
        try:
            re.compile(str(det.get("match", "")))
        except re.error as exc:
            errs.append(f"INV-8: detector regex does not compile ({exc})")
    elif det.get("type") == "exit-code" and not isinstance(det.get("match"), int):
        errs.append("INV-8: exit-code detector requires an integer match")

    # INV-4 — no embedded payloads / ANSI junk
    excerpt = doc.get("evidence", {}).get("crash_excerpt", "")
    if len(excerpt) > 512:
        errs.append("INV-4: crash_excerpt exceeds 512 characters")
    if ANSI_RE.search(excerpt):
        errs.append("INV-4: crash_excerpt contains raw ANSI escapes")

    # INV-9 — integrity
    if "integrity" in doc:
        want = doc["integrity"].get("value")
        got = body_digest(doc)
        if want != got:
            errs.append(f"INV-9: integrity mismatch (declared {str(want)[:12]}…, computed {got[:12]}…)")

    return errs


def cmd_validate(args) -> int:
    try:
        import jsonschema
    except ImportError:  # pragma: no cover
        print("ERROR: jsonschema required (pip install jsonschema)", file=sys.stderr)
        return 2

    schema = load_json(Path(args.schema))
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())

    files = [Path(p) for p in args.files]
    if not files:
        print("ERROR: no files given", file=sys.stderr)
        return 2

    seen_ids: dict[str, str] = {}
    failures = 0
    counts = {"draft": 0, "validated": 0, "revoked": 0}

    for path in files:
        doc = load_json(path)
        problems = [f"schema: {'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
                    for e in sorted(validator.iter_errors(doc), key=lambda e: list(e.path))]
        if not problems:
            problems = check_invariants(doc, seen_ids)
        counts[doc.get("status", "draft")] = counts.get(doc.get("status", "draft"), 0) + 1

        level_ok = True
        if args.level >= 3 and doc.get("status") != "validated":
            problems.append("L3: document is not validated")
            level_ok = False

        if problems:
            failures += 1
            print(f"✗ {path.name}")
            for p in problems[:6]:
                print(f"    - {p}")

    total = len(files)
    label = {1: "L1 well-formed", 2: "L2 semantically valid", 3: "L3 verified"}[args.level]
    if failures:
        print(f"\nFAIL ({label}): {failures}/{total} documents rejected")
        return 1

    print(f"OK ({label}): {total}/{total} documents accepted "
          f"· {counts.get('validated', 0)} validated · {counts.get('draft', 0)} draft · {counts.get('revoked', 0)} revoked")
    return 0


# --------------------------------------------------------------------------- #
# digest
# --------------------------------------------------------------------------- #

def cmd_digest(args) -> int:
    doc = load_json(Path(args.file))
    computed = body_digest(doc)
    declared = doc.get("integrity", {}).get("value")
    print(f"file     : {args.file}")
    print(f"computed : {computed}")
    print(f"declared : {declared}")
    if declared != computed:
        print("✗ MISMATCH — document does not match its integrity digest")
        return 1
    print("✓ digest verified")
    return 0


# --------------------------------------------------------------------------- #
# cli
# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description="ABX reference implementation (RFC-0)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("convert", help="corpus manifests -> ABX documents")
    c.add_argument("--corpus", default="corpus")
    c.add_argument("--out", default="corpus/abx")
    c.add_argument("--only", nargs="*", help="restrict to these antibody ids")
    c.add_argument("--all", action="store_true", help="convert the whole corpus (default)")
    c.add_argument("--check", action="store_true", help="verify rendered docs match sources; no writes")
    c.set_defaults(func=cmd_convert)

    v = sub.add_parser("validate", help="validate ABX documents")
    v.add_argument("files", nargs="*", help="paths to .abx.json documents")
    v.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    v.add_argument("--level", type=int, choices=(1, 2, 3), default=2)
    v.set_defaults(func=cmd_validate)

    d = sub.add_parser("digest", help="verify the integrity digest of one document")
    d.add_argument("file")
    d.set_defaults(func=cmd_digest)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
