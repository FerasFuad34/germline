# AB-000006 — libxml2: Heap-double-free in libxml2_xml_reader_for_file_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libxml2` |
| Class / CWE | `memory-safety` / CWE-415 |
| Sanitizer | `asan` |
| Crash type | `Heap-double-free` |
| Severity | High |
| Fixed in | [26828cb3a129](https://gitlab.gnome.org/GNOME/libxml2/-/commit/26828cb3a1294e09e42064f4769d4b3c0a8623b3) |
| Upstream report | https://issues.oss-fuzz.com/issues/42472675 |
| Dataset | ARVO localId `42472675` |

## What this antibody guards

This is the historical vulnerability **Heap-double-free** in `libxml2`
(fuzz target: `libxml2_xml_reader_for_file_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42472675-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42472675-fix arvo
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
