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

## Incident #001 — 2026-10-14 · environment-error (run 38638148330)

**Symptom.** The push-triggered double-check (run 38638148330) reported
`environment-error` for AB-000001…AB-000003 in ~12 ms each; workflow exit 1.

**Root cause.** The per-antibody wrapper (`corpus/antibodies/*/double-check.sh`)
delegates via `exec` to `tools/double-check-one.sh`. A workspace/snapshot
round-trip stripped the executable bit from that tool, so `exec` failed with
"Permission denied" (exit 126) before Docker was ever consulted. The verdict
class was *correct* (this is not a `mismatch`, i.e. no antibody is wrong), and
the workflow failed loudly instead of reporting false success — by design.

**Fix (committed at run #003):**
1. wrappers now delegate with `exec bash …` — robust to a missing exec bit;
2. executable bits restored on all shipped scripts (`chmod +x`, mode changes tracked in git);
3. a CI hygiene step now fails any run where a shipped script lacks the executable bit;
4. a Docker-free `--dry-run` smoke check runs on every push.

**Policy note.** Environment errors are never recorded as verdicts. They are
investigated, root-caused, and documented here — nothing is silently retried.

## Run #003 — 2026-10-14 · GitHub Actions (run 38638413451) — post-incident re-verification

| Antibody | Verdict | Note |
|---|---|---|
| `AB-000001` | ✅ verified | 3rd consecutive independent verification |
| `AB-000002` | ✅ verified | 3rd consecutive |
| `AB-000003` | ✅ verified | 2nd consecutive |

- **Result:** 3 verified · 0 mismatch · 0 errors — Incident #001 is closed.
- **Cumulative:** 3 antibodies validated, each reproduced across multiple runs.
