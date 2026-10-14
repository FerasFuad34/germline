# GERMLINE Antibody Corpus — v0.1

**100 reproducible security antibodies** derived from fixed, publicly disclosed
vulnerabilities — each one an executable check that must *fail* on a vulnerable
build and *pass* on the fixed build.

> SBOM tells you what's in your code. GERMLINE tells you what your code survived —
> and proves the next generation still survives it.

## What is in this package

| Path | What |
|---|---|
| `corpus/antibodies/AB-*/` | 100 antibody records: `manifest.yaml`, `meta.json`, `README.md`, `double-check.sh` |
| `corpus/abx/` | The same 100 antibodies in **ABX v0.1** wire format ([RFC-0](docs/rfc/0001-abx-antibody-exchange-format.md)) |
| `corpus/stats.json`, `INDEX.md` | Corpus statistics and a browsable index |
| `corpus/VERIFICATION.md`, `verification-state.json` | Append-only verification log (3 antibodies validated end-to-end at v0.1) |
| `schema/abx-0.1.schema.json` | Strict JSON Schema for the exchange format |
| `tools/abx.py` | Reference implementation: `convert`, `validate` (L1–L3), `digest` |
| `DATASHEET.md` | Full documentation of composition, collection and cleaning |
| `MANIFEST.sha256` | SHA-256 of every file in this package |
| `BUILD.json` | Build provenance (source commit, counts) |

## Quick start

```bash
# Validate all 100 documents against the schema + invariants (no Docker needed)
python3 tools/abx.py validate corpus/abx/*.abx.json

# Check a single document's integrity digest
python3 tools/abx.py digest corpus/abx/AB-000001.abx.json

# Re-run one antibody's verification (requires Docker)
bash corpus/antibodies/AB-000001/double-check.sh
```

## Licenses

- **Data** (`corpus/`, `DATASHEET.md`): CC-BY-4.0 — attribute ARVO (EuroS&P 2026)
  and OSS-Fuzz as upstream sources, and this corpus as the derived work.
- **Code** (`tools/`, `schema/`): Apache-2.0.
- **Specification** (`docs/rfc/`): open, no patent restrictions.

## Citation

Until a DOI is minted, cite the GitHub release:

> GERMLINE Project (2026). *GERMLINE Antibody Corpus v0.1* [Data set].
> https://github.com/FerasFuad34/germline

A Zenodo DOI will be attached to this release (see `CITATION.cff`).

## Policy

Only **fixed, publicly disclosed** vulnerabilities are included. No zero-days,
no embargoed research, no exploit payloads — records reference public OSS-Fuzz
reports and upstream fix commits (see `NOTICE.md`).
