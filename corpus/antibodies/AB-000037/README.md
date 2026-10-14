# AB-000037 — imagemagick: Heap-buffer-overflow READ 4 in encoder_j2k_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `imagemagick` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ 4` |
| Severity | Medium |
| Fixed in | [75477483fbf9](https://github.com/imagemagick/imagemagick/commit/75477483fbf99382b4310233b1521cbcc5e7affd) |
| Upstream report | https://issues.oss-fuzz.com/issues/42473556 |
| Dataset | ARVO localId `42473556` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ 4** in `imagemagick`
(fuzz target: `encoder_j2k_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42473556-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42473556-fix arvo
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
