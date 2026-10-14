# AB-000095 — openssl: Heap-buffer-overflow READ 14 in x509

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `openssl` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ 14` |
| Severity | Medium |
| Fixed in | [aec9667bd19a](https://github.com/openssl/openssl/commit/aec9667bd19a8ca9bdd519db3a231a95b9e92674) |
| Upstream report | https://issues.oss-fuzz.com/issues/42478556 |
| Dataset | ARVO localId `42478556` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ 14** in `openssl`
(fuzz target: `x509`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42478556-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42478556-fix arvo
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
