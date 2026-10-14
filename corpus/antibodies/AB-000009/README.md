# AB-000009 — libxml2: Stack-buffer-overflow WRITE {*} in libxml2_xml_read_memory_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libxml2` |
| Class / CWE | `memory-safety` / CWE-121 |
| Sanitizer | `asan` |
| Crash type | `Stack-buffer-overflow WRITE {*}` |
| Severity | High |
| Fixed in | [932cc9896ab4](https://gitlab.gnome.org/GNOME/libxml2/-/commit/932cc9896ab41475d4aa429c27d9afd175959d74) |
| Upstream report | https://issues.oss-fuzz.com/issues/42480782 |
| Dataset | ARVO localId `42480782` |

## What this antibody guards

This is the historical vulnerability **Stack-buffer-overflow WRITE {*}** in `libxml2`
(fuzz target: `libxml2_xml_read_memory_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42480782-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42480782-fix arvo
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
