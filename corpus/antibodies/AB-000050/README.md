# AB-000050 — harfbuzz: UNKNOWN READ in hb-shape-fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `harfbuzz` |
| Class / CWE | `memory-safety` / — |
| Sanitizer | `ubsan` |
| Crash type | `UNKNOWN READ` |
| Severity | Medium |
| Fixed in | [ca54eba4846d](https://github.com/harfbuzz/harfbuzz/commit/ca54eba4846d0afda4601929556617a7ebe51714) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470990 |
| Dataset | ARVO localId `42470990` |

## What this antibody guards

This is the historical vulnerability **UNKNOWN READ** in `harfbuzz`
(fuzz target: `hb-shape-fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   UndefinedBehaviorSanitizer:DEADLYSIGNAL
docker run --rm n132/arvo:42470990-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470990-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`UndefinedBehaviorSanitizer:DEADLYSIGNAL` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
