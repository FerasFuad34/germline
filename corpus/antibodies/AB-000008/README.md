# AB-000008 — libxml2: Heap-use-after-free READ 8 in libxml2_xml_reader_for_file_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libxml2` |
| Class / CWE | `memory-safety` / CWE-416 |
| Sanitizer | `asan` |
| Crash type | `Heap-use-after-free READ 8` |
| Severity | High |
| Fixed in | [664f881008f4](https://gitlab.gnome.org/GNOME/libxml2/-/commit/664f881008f40356c0502c8cc154e17e3c80e353) |
| Upstream report | https://issues.oss-fuzz.com/issues/42478580 |
| Dataset | ARVO localId `42478580` |

## What this antibody guards

This is the historical vulnerability **Heap-use-after-free READ 8** in `libxml2`
(fuzz target: `libxml2_xml_reader_for_file_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42478580-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42478580-fix arvo
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
