# AB-000005 — libxml2: Bad-free in libxml2_xml_reader_for_file_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libxml2` |
| Class / CWE | `memory-safety` / CWE-590 |
| Sanitizer | `asan` |
| Crash type | `Bad-free` |
| Severity | Medium |
| Fixed in | [1567b55b72b8](https://gitlab.gnome.org/GNOME/libxml2/-/commit/1567b55b72b8366ce120ed042e03ed5b50d191d7) |
| Upstream report | https://issues.oss-fuzz.com/issues/42471662 |
| Dataset | ARVO localId `42471662` |

## What this antibody guards

This is the historical vulnerability **Bad-free** in `libxml2`
(fuzz target: `libxml2_xml_reader_for_file_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42471662-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42471662-fix arvo
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
