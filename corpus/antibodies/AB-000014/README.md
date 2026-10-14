# AB-000014 — libxml2: Bad-cast in xml

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libxml2` |
| Class / CWE | `memory-safety` / CWE-704 |
| Sanitizer | `ubsan` |
| Crash type | `Bad-cast` |
| Severity | High |
| Fixed in | [bfd2f4300fb3](https://gitlab.gnome.org/GNOME/libxml2/-/commit/bfd2f4300fb348a0fb8265a17546a0eb8bdec719) |
| Upstream report | https://issues.oss-fuzz.com/issues/42496802 |
| Dataset | ARVO localId `42496802` |

## What this antibody guards

This is the historical vulnerability **Bad-cast** in `libxml2`
(fuzz target: `xml`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   runtime error:
docker run --rm n132/arvo:42496802-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42496802-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`runtime error:` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
