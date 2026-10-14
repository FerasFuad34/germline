# AB-000022 — ffmpeg: UNKNOWN WRITE in ffmpeg_AV_CODEC_ID_HYMT_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `ffmpeg` |
| Class / CWE | `memory-safety` / — |
| Sanitizer | `ubsan` |
| Crash type | `UNKNOWN WRITE` |
| Severity | High |
| Fixed in | [ab160efa2850](https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff/ab160efa2850715de32e24fed846a0f6ef7244ab) |
| Upstream report | https://issues.oss-fuzz.com/issues/42472621 |
| Dataset | ARVO localId `42472621` |

## What this antibody guards

This is the historical vulnerability **UNKNOWN WRITE** in `ffmpeg`
(fuzz target: `ffmpeg_AV_CODEC_ID_HYMT_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   UndefinedBehaviorSanitizer:DEADLYSIGNAL
docker run --rm n132/arvo:42472621-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42472621-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`UndefinedBehaviorSanitizer:DEADLYSIGNAL` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
