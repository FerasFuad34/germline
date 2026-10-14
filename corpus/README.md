# 📦 GERMLINE Antibody Corpus

**100 antibodies** (draft) across **17 critical open-source projects** — generated from
[ARVO](https://github.com/n132/ARVO-Meta) (Atlas of Reproducible Vulnerabilities, EuroS&P 2026),
which builds on Google's OSS-Fuzz.

> **Status: 🟡 draft** — every antibody must pass the **double-check**
> (crash on the vulnerable build **with the expected marker** / clean on the fixed build)
> before it can be marked `validated`. See [INDEX.md](INDEX.md) for the full list.

## What is an antibody?

A self-contained, portable regression test derived from a **fixed, publicly disclosed** vulnerability:

```
corpus/antibodies/AB-000042/
├── manifest.yaml     # machine-readable: source, attack, test, provenance, evidence hash
├── README.md         # what it guards + exactly how to reproduce
├── meta.json         # raw ARVO record + docker images + expected crash excerpt
└── double-check.sh   # canonical validation wrapper
```

A descendant code generation (fork, patch, **AI rewrite**, translation) is *immune* to a
historical vulnerability only if it replays this antibody and stays clean.

## Double-check (the rule that makes this corpus credible)

```bash
# validate a sample (needs Docker):
bash tools/run-corpus-checks.sh --sample 5 --report out/verification.json

# one antibody:
bash tools/run-corpus-checks.sh --only AB-000001

# integrity-only, no Docker (CI-friendly, fast):
bash tools/run-corpus-checks.sh --dry-run
```

Verdicts: `verified` · `mismatch` (must be fixed or revoked) · `environment-error`.
Semantics: the vulnerable image must produce the recorded sanitizer marker
(`ERROR: AddressSanitizer` / `WARNING: MemorySanitizer` / `runtime error:`),
and the fixed image must **not**.

## Automated verification runs

The **Corpus double-check** workflow runs on GitHub's Docker runners:
on demand (Actions → Run workflow), weekly (sample of 2), and **automatically whenever a
commit touches `corpus/`** (checking the changed antibodies first, capped at 3 per run).
Each run uploads `verification.json` as an artifact.

## Selection (first batch)

Chosen for storytelling + diversity (17 projects, 15 crash types, 3 sanitizers, 26 High-severity):

| Project | N | Project | N |
|---|---|---|---|
| libxml2 | 14 | libarchive | 5 |
| ffmpeg | 14 | gpac | 4 |
| imagemagick | 12 | binutils-gdb | 4 |
| harfbuzz | 10 | freetype2 | 3 |
| curl | 8 | openssl | 3 |
| wireshark | 7 | libwebp | 2 |
| ghostpdl | 6 | zlib · libpng · libtiff | 1 each |
| php-src | 5 | | |

## Provenance & licenses

- Upstream dataset: **ARVO** (OSS-Fuzz). Each antibody records: OSS-Fuzz issue URL,
  fix commit, patch URL, project repo, docker images, and a SHA-256 of the expected crash output.
- Corpus metadata: **CC-BY-4.0** with attribution. Tooling: Apache-2.0.
- **Policy:** fixed & publicly disclosed vulnerabilities only. No live 0-days. No exploits
  distributed — only *tests* that reproduce already-fixed bugs.

## Regenerating

```bash
# 1) download arvo.db (v3.0.0, 162 MB) from github.com/n132/ARVO-Meta/releases
# 2) regenerate (stable IDs via corpus/id-map.json):
python3 extractor/arvo.py --db /path/to/arvo.db --out corpus --selection extractor/selection.yaml
```

IDs are **stable**: re-running never reshuffles existing antibodies.

---

## ABX export (RFC-0)

The corpus is published twice: as human-friendly authoring manifests (above) and
as **ABX v0.1 wire documents** in [`abx/`](abx/) — the strict, canonicalizable
exchange format specified in [RFC-0](../docs/rfc/0001-abx-antibody-exchange-format.md).

```bash
python3 tools/abx.py convert --corpus corpus --out corpus/abx --all   # manifests -> ABX
python3 tools/abx.py validate corpus/abx/*.abx.json                   # L2: schema + invariants
python3 tools/abx.py digest corpus/abx/AB-000001.abx.json             # integrity check
```

One source of truth, two renderings: `--check` fails if the ABX documents ever
drift from their manifests (enforced in CI). Verified antibodies appear as
`status: validated` with an append-only `verification.runs` history.
