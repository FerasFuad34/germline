# AB-000038 — imagemagick: Heap-use-after-free WRITE 4 in encoder_mat_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `imagemagick` |
| Class / CWE | `memory-safety` / CWE-416 |
| Sanitizer | `asan` |
| Crash type | `Heap-use-after-free WRITE 4` |
| Severity | High |
| Fixed in | [f7206618d27c](https://github.com/imagemagick/imagemagick/commit/f7206618d27c2e69d977abf40e3035a33e5f6be0) |
| Upstream report | https://issues.oss-fuzz.com/issues/42474040 |
| Dataset | ARVO localId `42474040` |

## What this antibody guards

This is the historical vulnerability **Heap-use-after-free WRITE 4** in `imagemagick`
(fuzz target: `encoder_mat_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42474040-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42474040-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`ERROR: AddressSanitizer` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
