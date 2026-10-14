# AB-000048 — harfbuzz: Use-of-uninitialized-value in hb-shape-fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `harfbuzz` |
| Class / CWE | `memory-safety` / CWE-457 |
| Sanitizer | `msan` |
| Crash type | `Use-of-uninitialized-value` |
| Severity | Medium |
| Fixed in | [f8ccb545c47a](https://github.com/harfbuzz/harfbuzz/commit/f8ccb545c47abe8f0f4ed318ff7b5bf176913893) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470405 |
| Dataset | ARVO localId `42470405` |

## What this antibody guards

This is the historical vulnerability **Use-of-uninitialized-value** in `harfbuzz`
(fuzz target: `hb-shape-fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   WARNING: MemorySanitizer
docker run --rm n132/arvo:42470405-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470405-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`WARNING: MemorySanitizer` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
