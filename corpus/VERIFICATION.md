# 📋 Corpus Verification Log

Every entry records an actual execution of the double-check
(**crash on vulnerable image with the expected marker / clean on fixed image**)
on a Docker host. This log is the credible record of corpus validity.

## Run #001 — 2026-10-14 · GitHub Actions (`Corpus double-check`, run 38630272283)

**Mechanism: operational.** First antibodies validated end-to-end in CI (Docker on GitHub runners).

| Antibody | Project | Sanitizer | Crash type | Vulnerable | Fixed | Verdict |
|---|---|---|---|---|---|---|
| `AB-000001` | libxml2 | msan | Use-of-uninitialized-value | crash (`WARNING: MemorySanitizer`) | clean | ✅ verified |
| `AB-000002` | libxml2 | msan | Use-of-uninitialized-value | crash (`WARNING: MemorySanitizer`) | clean | ✅ verified |

- **Result:** 2 verified · 0 mismatch · 0 errors (report: `verification.json` artifact)
- **Timing:** ~40s and ~11s per antibody (incl. image pull) — full-corpus pass is feasible.
- **Trigger:** automatic on pushes touching `corpus/` or `tools/`; also manual
  (Actions → *Corpus double-check* → Run workflow) and weekly (sample of 2).

### How to extend this log

```bash
# locally (Docker required):
bash tools/run-corpus-checks.sh --sample 10 --report out/verification.json

# or on GitHub: Actions → "Corpus double-check" → Run workflow → sample: 10
```

When an antibody passes verification, its `manifest.yaml` status is promoted
`draft → validated` and the antibody is appended to the log above with its run reference.
Mismatches are handled as incidents: fixed, re-verified, or **revoked** (never silently kept).

---
*Policy reminder: antibodies derive from **fixed, publicly disclosed** vulnerabilities only.*

## Run #002 — 2026-10-14 · GitHub Actions (`Corpus double-check`, run 38635106574)

Triggered automatically by the RFC-0 commit (`bcc5078`), scope = first 3 changed antibodies.

| Antibody | Project | Sanitizer | Vulnerable | Fixed | Verdict |
|---|---|---|---|---|---|
| `AB-000001` | libxml2 | msan | crash | clean | ✅ verified |
| `AB-000002` | libxml2 | msan | crash | clean | ✅ verified |
| `AB-000003` | libxml2 | msan | crash | clean | ✅ verified |

- **Result:** 3 verified · 0 mismatch · 0 errors — repeatability across runs (AB-000001/2 verified twice).
- **Cumulative:** 3 antibodies validated out of 100.
