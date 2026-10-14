# 🧬 GERMLINE — Public Roadmap

> **SBOM tells you what's in your code. GERMLINE tells you what your code survived — and proves the next generation still survives it.**
> Status: **pre-alpha** · Working name: GERMLINE · Everything below is a commitment only when marked so.

---

## What we are building (in one breath)

A portability layer for **security inheritance** across code generations:
1. **Antibody Corpus** — historical vulnerabilities turned into executable, permanently reproducible regression antibodies.
2. **Immune Gate** — a CI/CD gate that replays every ancestor's antibodies against any descendant (rewrite, fork, translation) and issues a signed **Immune Passport**.
3. **ABX** — an open spec (`Antibody eXchange`) for sharing antibodies across organizations and vendors.

Only **fixed, publicly disclosed** vulnerabilities are ever included. We do not disclose, exploit, or distribute working attacks against live systems.

---

## Milestones

### M0 — Foundation `target: Oct 2026`
- [x] Antibody extractor + **100 draft antibodies** from ARVO across 17 critical projects (stable IDs, provenance, evidence hashes)
- [~] Double-check the corpus (crash-on-vulnerable / clean-on-fixed): **mechanism operational — 3/100 verified in CI** (runs #001–#002, repeatable; see `corpus/VERIFICATION.md`); full-corpus pass being scheduled
- [x] **RFC-0: `ABX` antibody exchange format v0.1** — spec ([docs/rfc](docs/rfc/0001-abx-antibody-exchange-format.md)) + strict JSON Schema + reference validator + 100-document conformance corpus, open for public review
- [x] Public repo: LICENSE (Apache-2.0), Security Policy, Threat Model, Code of Conduct
- [ ] Own SBOM + self-immune-passport on every release (we use what we sell)

### M1 — Proof `Nov – Dec 2026`
- [x] Extractor v0.1 (public, Apache-2.0)
- [ ] Dataset v0.1 with DOI (Zenodo) + datasheet
- [ ] Immune Gate GitHub Action — beta with 3 OSS pilot repos
- [ ] First public monthly Immune Digest

### M2 — The Case Study `Jan – Feb 2027`
- [ ] **Immune Amnesia Experiment #1**: measure inherited-protection loss across a real AI-assisted C→Rust rewrite of a well-known library
- [ ] Publish results — including negative results
- [ ] ≥1 real, documented immune amnesia finding (else: scope pivot, publicly explained)

### M3 — Global Launch `Mar – Apr 2027`
- [ ] Preprint (arXiv) + replication package
- [ ] Show HN / r/netsec launch
- [ ] Conference submissions: Black Hat Arsenal, FOSDEM, BSides — demo-ready

### M4 — First Paid Work `May – Jul 2027`
- [ ] CRA compliance report generator (CLI → signed PDF)
- [ ] First 2 paid design-partner engagements (legacy-heritage audit for Rust migrations)

### M5 — Company `Aug – Oct 2027` (committed)
- [ ] Legal entity + payment rails
- [ ] Registry Cloud GA ahead of the EU CRA full-application date (11 Dec 2027)
- [ ] 3 recurring customers

---

## North Star metric

**Verified antibodies** — reproduced, double-checked (fail-on-vulnerable / pass-on-fixed), signed, and reused across real descendant generations. Stars, followers, and talks are secondary.

## How to get involved (when M1 lands)
- Bring a library: we will run a free immune audit of a real project's lineage.
- Bring an antibody: open an issue with `type: antibody` and a reproducible source.
- Bring a counterexample: falsification of any published result is rewarded with public credit.

## License
Code: Apache-2.0 · Dataset: CC-BY-4.0 · Spec: OWF-1.0 (copyright only, no patent restrictions).
