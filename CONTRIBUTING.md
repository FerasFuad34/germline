# Contributing to GERMLINE

Thanks for helping build security inheritance for software. Read this before opening a PR — the rules are strict **by design**, because credibility is the product.

## The three laws

1. **Fixed and public only.** Every antibody must derive from a vulnerability that is *fixed* and *publicly disclosed* (ARVO / OSS-Fuzz / CVE / vendor advisory). PRs referencing live 0-days are closed immediately.
2. **Reproducible or it doesn't exist.** Every antibody must run in a pinned container and must **fail on the vulnerable revision and pass on the fixed revision**, automatically. No manual "it worked on my machine."
3. **Sign your commits.** Use `git commit -s` (Developer Certificate of Origin). Unsigned-off commits will be asked to amend.

## Adding an antibody (`type: antibody`)

1. Open an issue with the template first (keeps review cheap).
2. Create `corpus/antibodies/AB-XXXXXX/` containing:
   - `manifest.yaml` — per `spec/` (RFC-0)
   - `input` — the triggering input (or a pinned generator)
   - `README.md` — one screen: what it is, how to run it, provenance
3. Run the double-check locally:
   ```bash
   ./tools/double-check.sh AB-XXXXXX   # fails on vulnerable / passes on fixed
   ```
4. Open the PR. CI will re-run the double-check on a clean container — CI verdict wins over local results.

**Anti-patterns that get a PR rejected:** flaky inputs, tests that pass in both revisions, tests requiring network access at runtime, tests depending on unpinned external services.

## Code contributions

- Languages: Python (tooling), YAML (corpus), Shell (glue). Rust may come later for the gate.
- Style: keep it boring and readable; type hints in Python; no new heavyweight dependencies without discussion.
- Every PR: `make test` green + CHANGELOG entry for user-visible changes.
- Commit messages: `area: imperative summary` (e.g., `extractor: handle multi-hunk patch metadata`).

## Review process

| Change | Required review |
|---|---|
| New antibody | 1 maintainer + CI double-check |
| Antibody modification | 1 maintainer + rationale in PR (antibodies are append-only in spirit; corrections are new versions) |
| Spec (ABX) | Public comment period (per RFC process in `spec/`) |
| Threat model changes | 1 maintainer + Security section of PR template filled |

## Licensing

By contributing you agree: code under Apache-2.0, corpus data under CC-BY-4.0, spec contributions under the spec's open license. You keep your copyright; you grant the project the right to redistribute under those terms.

## Conduct

All participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
