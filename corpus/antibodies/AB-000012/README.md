# AB-000012 — libxml2: Heap-use-after-free READ 8 in xml

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libxml2` |
| Class / CWE | `memory-safety` / CWE-416 |
| Sanitizer | `asan` |
| Crash type | `Heap-use-after-free READ 8` |
| Severity | High |
| Fixed in | [19cae17f5a2a](https://gitlab.gnome.org/GNOME/libxml2/-/commit/19cae17f5a2acfbd5554d145bb87cd6bf2de244f) |
| Upstream report | https://issues.oss-fuzz.com/issues/42486665 |
| Dataset | ARVO localId `42486665` |

## What this antibody guards

This is the historical vulnerability **Heap-use-after-free READ 8** in `libxml2`
(fuzz target: `xml`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42486665-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42486665-fix arvo
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
