# AB-000060 — wireshark: Heap-buffer-overflow READ 1 in fuzzshark_ip_proto-udp

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `wireshark` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ 1` |
| Severity | Medium |
| Fixed in | [38657fad5803](https://github.com/wireshark/wireshark/commit/38657fad58034ff5557caef10ef679b4ac404dbd) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470194 |
| Dataset | ARVO localId `42470194` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ 1** in `wireshark`
(fuzz target: `fuzzshark_ip_proto-udp`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42470194-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470194-fix arvo
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
