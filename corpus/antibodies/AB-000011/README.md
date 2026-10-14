# AB-000011 — libxml2: Heap-use-after-free READ 4 in xml

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libxml2` |
| Class / CWE | `memory-safety` / CWE-416 |
| Sanitizer | `asan` |
| Crash type | `Heap-use-after-free READ 4` |
| Severity | High |
| Fixed in | [dba82a8c0453](https://gitlab.gnome.org/GNOME/libxml2/-/commit/dba82a8c0453b7d4d138167a771c1c2988b889be) |
| Upstream report | https://issues.oss-fuzz.com/issues/42486565 |
| Dataset | ARVO localId `42486565` |

## What this antibody guards

This is the historical vulnerability **Heap-use-after-free READ 4** in `libxml2`
(fuzz target: `xml`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42486565-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42486565-fix arvo
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
