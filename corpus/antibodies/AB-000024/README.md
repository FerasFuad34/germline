# AB-000024 — ffmpeg: Heap-buffer-overflow READ 4 in ffmpeg_AV_CODEC_ID_HYMT_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `ffmpeg` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ 4` |
| Severity | Medium |
| Fixed in | [fcbda8af175a](https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff/fcbda8af175a1f305c46d6d46a4f90be4aa630ae) |
| Upstream report | https://issues.oss-fuzz.com/issues/42472718 |
| Dataset | ARVO localId `42472718` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ 4** in `ffmpeg`
(fuzz target: `ffmpeg_AV_CODEC_ID_HYMT_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42472718-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42472718-fix arvo
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
