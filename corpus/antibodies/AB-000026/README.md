# AB-000026 — ffmpeg: Heap-buffer-overflow WRITE 8 in ffmpeg_AV_CODEC_ID_TIERTEXSEQVIDEO_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `ffmpeg` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `ubsan` |
| Crash type | `Heap-buffer-overflow WRITE 8` |
| Severity | High |
| Fixed in | [ce551a3925a1](https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff/ce551a3925a1cf9c7824e26a246b99b6773bda4b) |
| Upstream report | https://issues.oss-fuzz.com/issues/42473850 |
| Dataset | ARVO localId `42473850` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow WRITE 8** in `ffmpeg`
(fuzz target: `ffmpeg_AV_CODEC_ID_TIERTEXSEQVIDEO_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   [1m[31m==7==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7ffff7e62838 at pc 0x000000550395 bp 0x7fffffff
docker run --rm n132/arvo:42473850-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42473850-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`[1m[31m==7==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7ffff7e62838 at pc 0x000000550395 bp 0x7fffffff` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
