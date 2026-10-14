# Datasheet — GERMLINE Antibody Corpus v0.1

*Following the "Datasheets for Datasets" structure (Gebru et al.), adapted for a
security-regression corpus.*

Version: **0.1.0** · Date: **2026-10-14** · License: **CC-BY-4.0 (data) /
Apache-2.0 (code)** · Maintainer: GERMLINE project.

---

## 1. Motivation

**Why was this dataset created?**
Software rewrites — especially AI-assisted translation between languages — can
silently drop security properties that older code had. Existing artifacts (CVEs,
patches, SBOMs, scanners) describe vulnerabilities but do not provide a *reusable
experiment* that proves whether a given build still resists them. This corpus
turns historical vulnerabilities into machine-readable, permanently reproducible
**antibodies**: one vulnerable environment that must fail, one fixed environment
that must stay clean, plus the evidence that this discrimination has been measured.

**Who created it and who funded it?**
The GERMLINE project (independent, pre-alpha, grant-seeking). The corpus is
derived from **ARVO** (Atlas of Reproducible Vulnerabilities, EuroS&P 2026),
which curates **OSS-Fuzz** reports.

**Any other comments?**
The dataset is policy-bounded: **fixed, publicly disclosed vulnerabilities only**.

## 2. Composition

**What do the instances represent?**
Each instance ("antibody") is one historical memory-safety vulnerability in a
C/C++ open-source project, rendered as two formats: an authoring manifest and an
ABX v0.1 exchange document.

**How many instances?** 100 antibodies across 17 projects.

| Property | Distribution |
|---|---|
| Projects | 17 — libxml2 14 · ffmpeg 14 · imagemagick 12 · harfbuzz 10 · curl 8 · wireshark 7 · ghostpdl 6 · php-src 5 · libarchive 5 · gpac 4 · binutils-gdb 4 · freetype2 3 · openssl 3 · libwebp 2 · zlib 1 · libpng 1 · libtiff 1 |
| Sanitizer | asan 76 · msan 14 · ubsan 10 |
| Severity (upstream) | High 26 · Medium 74 |
| Weakness class | memory-safety 100 |
| Top CWEs | CWE-122 ×30 · CWE-457 ×13 · CWE-416 ×13 · CWE-119 ×11 · CWE-121 ×5 · CWE-129 ×4 |
| Crash-type variety | 39 distinct types |

**What does each instance contain?**

- Identity: stable ID (`AB-000001…AB-000100`), immutable and never reused.
- Subject: project, upstream repository, language, generation, fixed-in commit.
- Vulnerability: OSS-Fuzz report id, CWE(s), crash type, sanitizer, severity.
- Challenge: harness command, target fuzz function, expected observations
  (`vulnerable: crash` / `fixed: clean`), positive failure detector.
- Environments: pinned OCI image references (`n132/arvo:<id>-vul` and `-fix`).
- Evidence: report URL, patch URL, fix commit, SHA-256 of the expected crash
  output, ≤512-character fair-use excerpt.
- Provenance: ARVO dataset version + record id, generator, generation timestamp,
  license.
- Verification: append-only run history with verdicts
  (`verified` / `mismatch` / `environment-error`).

**Is everything public?**
Yes. Instances reference public OSS-Fuzz issues and upstream fix commits; no
non-public vulnerability data is included. **No personal data** is present.

## 3. Collection process

Source: **ARVO v3.0.0** (`arvo.db`, 6,138 records; all with `reproduced=1` and
`patch_located=1`), itself derived from OSS-Fuzz. Selection rules (deterministic):

1. 17 projects chosen for security centrality and ecosystem spread.
2. Cap of 2 records per (project, crash-type) pair to avoid monoculture.
3. Target of 100 records, filled in fixed project order with documented fallbacks.
4. IDs assigned in generation order through a stable id map (`id-map.json`);
   once assigned, an ID never changes meaning.

Binary artifacts (crash reproducers, images) are **not redistributed** here; the
corpus references them (OSS-Fuzz, `n132/arvo` OCI images) by identifier + digest.

## 4. Preprocessing / cleaning

Building the ABX rendering exposed three real data-quality defects in the
upstream metadata, all fixed at generation time (documented in the repository
history):

| Defect | Scale found | Resolution |
|---|---|---|
| Raw ANSI escape sequences inside detection markers | 1 record in corpus | stripped + whitespace collapsed; manifests are strict-parsable YAML |
| Multi-commit `fix_commit` fields (newline-separated hashes) | 394 ARVO records; 8 in corpus | first commit as the scalar value; full list preserved in `meta.json` (`fix_commits`) and in ABX `ext.germline.fix_commits` |
| Multi-line `fuzz_target` values | 3 ARVO records | first line retained |

**Verification-layer cleaning:** every generated document is validated against
the strict ABX schema plus invariants (discrimination, pinned environments,
integrity digest, append-only verification) in CI on every change.

## 5. Verification status (as of v0.1)

| Run | Date | Scope | Result |
|---|---|---|---|
| #001 | 2026-10-14 | AB-000001, AB-000002 | 2 verified · 0 mismatch · 0 errors |
| #002 | 2026-10-14 | AB-000001…AB-000003 | 3 verified · 0 mismatch · 0 errors |

**3 of 100 antibodies are `validated`** (executed on GitHub-hosted Docker:
crash with the expected marker on the vulnerable image, clean on the fixed one;
AB-000001/2 reproduced across two independent runs). The remaining 97 are
`draft` — generated and schema-valid but not yet self-verified. **Draft status is
explicit in every record**: absence of verification is never rendered as success.

## 6. Uses

**Intended uses**
- Regression antibodies for CI/CD ("immune gates") across code generations.
- Research on security-property inheritance in AI-assisted rewrites.
- Interoperability testing of the ABX format and validators.
- Teaching: complete, lawful, reproducible vulnerability case studies.

**Uses to avoid / cautions**
- The corpus concerns **historical, already-fixed** software versions only; it
  must not be used to claim anything about current versions of these projects.
- Verification executes container images: treat documents as untrusted
  instructions (sandbox, resource caps, no host mounts).
- Do not present draft records as verified evidence.

## 7. Distribution

- Source repository: https://github.com/FerasFuad34/germline
- Release artifact: `germline-corpus-v0.1.0.zip` (this package) + `MANIFEST.sha256`
- DOI: to be minted via Zenodo for the v0.1.0 release (metadata prepared in
  `dataset/metadata/zenodo-deposit.json`).
- Licenses: data CC-BY-4.0 (attribute ARVO + OSS-Fuzz + this corpus); code
  Apache-2.0; specification open, no patent restrictions.

## 8. Maintenance

- **Append-only IDs**: new antibodies take the next free ID; existing IDs are
  never renumbered or reused. Retraction is expressed as `status: revoked`.
- **Regeneration**: the corpus is deterministically regenerable from `arvo.db`
  plus `extractor/selection.yaml`; re-rendering the ABX layer is byte-stable
  (per-antibody first-generation timestamps are frozen).
- **Versioning**: corpus versions follow `v0.` increments until the format and
  verification process graduate to v1.0.
- **Contact**: via GitHub issues (labels `dataset`, `verification`, `rfc`).

## 9. Ethical and legal considerations

- Only publicly disclosed, fixed vulnerabilities are represented.
- No exploit payloads, binaries, or personal data are redistributed.
- Upstream projects' code and licenses are untouched; we reference, we do not
  relicense them.
- The dataset's purpose is defensive: preserving security properties across the
  rewrites and migrations that the industry is currently undergoing at speed.
