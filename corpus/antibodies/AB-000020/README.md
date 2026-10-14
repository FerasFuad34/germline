# AB-000020 — ffmpeg: Global-buffer-overflow READ 2 in ffmpeg_AV_CODEC_ID_ILBC_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `ffmpeg` |
| Class / CWE | `memory-safety` / CWE-119 |
| Sanitizer | `asan` |
| Crash type | `Global-buffer-overflow READ 2` |
| Severity | Medium |
| Fixed in | [e90f0ac334f2](https://git.ffmpeg.org/gitweb/ffmpeg.git/commitdiff/e90f0ac334f2bec0961955dceb824148594a4016) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470870 |
| Dataset | ARVO localId `42470870` |

## What this antibody guards

This is the historical vulnerability **Global-buffer-overflow READ 2** in `ffmpeg`
(fuzz target: `ffmpeg_AV_CODEC_ID_ILBC_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42470870-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470870-fix arvo
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
