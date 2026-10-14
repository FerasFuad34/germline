# AB-000093 — openssl: Stack-use-after-return READ 4 in client

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `openssl` |
| Class / CWE | `memory-safety` / CWE-562 |
| Sanitizer | `asan` |
| Crash type | `Stack-use-after-return READ 4` |
| Severity | Medium |
| Fixed in | [83b4a24384e6](https://github.com/openssl/openssl/commit/83b4a24384e62ed8cf91f51bf9a303f98017e13e) |
| Upstream report | https://issues.oss-fuzz.com/issues/42475667 |
| Dataset | ARVO localId `42475667` |

## What this antibody guards

This is the historical vulnerability **Stack-use-after-return READ 4** in `openssl`
(fuzz target: `client`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42475667-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42475667-fix arvo
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
