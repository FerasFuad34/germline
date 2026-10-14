# AB-000094 — openssl: Heap-buffer-overflow WRITE 1 in conf

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `openssl` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow WRITE 1` |
| Severity | High |
| Fixed in | [ed57f7f93508](https://github.com/openssl/openssl/commit/ed57f7f93508776b898e4c23b65d67f3479edaf1) |
| Upstream report | https://issues.oss-fuzz.com/issues/42476770 |
| Dataset | ARVO localId `42476770` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow WRITE 1** in `openssl`
(fuzz target: `conf`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42476770-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42476770-fix arvo
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
