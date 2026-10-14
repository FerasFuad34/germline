# NOTICE — provenance, attribution and responsible use

## Upstream sources

- **ARVO — Atlas of Reproducible Vulnerabilities** (EuroS&P 2026),
  https://github.com/n132/ARVO · https://github.com/n132/ARVO-Meta
  License: CC-BY-4.0. The GERMLINE corpus is a derived work: records were
  selected, normalized and rendered into a new format (ABX).
- **OSS-Fuzz** (Google), https://github.com/google/oss-fuzz — origin of the
  vulnerability reports referenced by each record.
- Individual upstream projects (libxml2, ffmpeg, ImageMagick, harfbuzz, curl, …):
  fix commits and repository URLs are referenced; their code and licenses are
  not modified or redistributed.

## What is redistributed here

Only metadata and derived documents: identifiers, URLs, digests, short
fair-use excerpts (≤512 characters) of machine-generated sanitizer output, and
reproduction *instructions*. No binaries, no crash inputs, no images.

## Responsible use

- Everything referenced is **fixed and publicly disclosed**.
- Verification runs execute third-party container images by design: run them
  sandboxed, without host mounts or default network access, with resource caps.
- Do not use `draft` records as evidence of anything except schema conformance.

## Attribution example

> Data derived from the GERMLINE Antibody Corpus v0.1 (CC-BY-4.0), which is
> derived from ARVO (EuroS&P 2026), which curates OSS-Fuzz reports.
