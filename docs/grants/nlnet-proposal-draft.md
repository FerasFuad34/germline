# NLnet / NGI Zero — Grant Application Draft
### Project: GENOME — Immune Inheritance for Software (ver. 0.1 draft)

> ⚠️ Apply pathway: https://nlnet.nl/apply — **current window closes 3 November 2026** (verify on site).
> Requested amount: **€30,000** over 6 months (first-time applicant range: €5k–€50k).
> This draft is a skeleton: fill `[TODO]` fields before submitting. Keep total length within the form's limits; NLnet accepts plain, factual, well-scoped proposals.

---

## 1. Abstract (≈150 words)

AI-assisted code rewrites are now routine: critical C/C++ libraries are being translated to memory-safe languages at scale (e.g., Google's AI-assisted giflib→Rust rewrite, DARPA TRACTOR). Each rewritten generation is a *new body with no immune memory*: it can silently lose protections its ancestor had already acquired through years of vulnerability fixes. Today, no tool measures or enforces the **inheritance of security protections across generations**.

GENOME builds the missing layer: (1) an **open corpus of executable "antibodies"** — permanently reproducible tests derived from fixed, publicly disclosed vulnerabilities (built on ARVO/OSS-Fuzz); (2) an **Immune Gate** in CI/CD that replays all ancestors' antibodies against any descendant and issues a **signed Immune Passport**; (3) **ABX**, an open exchange format so antibodies travel between organizations and vendors. Deliverables are free and open source, with a benchmark report measuring *immune amnesia* in real rewrites.

## 2. Who we are

[TODO: Name, location, role. Add: cybersecurity background, prototype status — the working immune-gate prototype exists and the author has already published a technical brief. Mention any academic affiliation or advisor.]

## 3. Prior work we build upon (honest positioning)

- ARVO (EuroS&P 2026): 6,100+ reproducible vulnerabilities with Docker builds, PoC triggers, and canonical patches — our antibody source.
- Vul4J / CWE-Bench-Java: reproducible Java vulnerability benchmarks with PoV tests (expansion path).
- Vulnerability *reintroduction* studies (ESEM 2022; ImageMagick case study 2026): measured **within one repository**. **Gap:** nobody measures inheritance **across generations, rewrites, and languages**.

## 4. Work packages (6 months)

| WP | Deliverable | Effort |
|---|---|---|
| WP1 | **Antibody extraction pipeline**: ARVO → validated antibodies (fail-on-vul/pass-on-fix), signed, versioned. Target: 500+ for release corpus. | €10,000 |
| WP2 | **Immune Gate v1**: GitHub Action + CLI; replay antibodies along a lineage graph; produce signed Immune Passport (Sigstore + transparency log). | €8,000 |
| WP3 | **ABX specification v0.1**: open RFC + reference implementation + community review; interoperability with SBOM/attestation ecosystems (SPDX/CycloneDX/in-toto). | €6,000 |
| WP4 | **The Immune Amnesia benchmark report**: measure protection loss across public AI-assisted/legacy rewrites; publish methodology, negative results, and a replication package (Zenodo DOI). | €4,000 |
| WP5 | **Community & governance**: threat model, datasheet, contribution guide, 2 public review rounds. | €2,000 |
| | **Total** | **€30,000** |

## 5. Why this fits NGI Zero / the commons

- **Standardization & deployability**: ABX becomes shared public infrastructure (like STIX for threat intel) rather than another vendor silo.
- **Security & auditing**: nothing is sold until it is measurable; every claim ships with a reproducible check.
- **Commons-first**: code Apache-2.0, data CC-BY-4.0, spec openly licensable; no patents; no lock-in.
- **Global South contribution**: built in Yemen, published globally — a direct example of the open internet enabling engineering capacity anywhere.

## 6. Risks & mitigation

| Risk | Mitigation |
|---|---|
| LLM-generated antibodies have false positives | Hard acceptance rule (double-check) + human review + published FP metrics |
| Poisoning of the antibody corpus | Signing, review, revocation, transparency log; document in threat model |
| Scope creep | One north-star metric: verified antibodies reused across real projects |

## 7. Budget notes

Individual grant, 6 months, part-time-plus effort. Budget covers engineering time only; infrastructure stays under €100/month (CI + storage on free/open tiers) and is not requested.

## 8. Sustainability beyond the grant

Open-core: the standard and corpus remain open forever; a hosted registry, CRA-compliance reporting, and legacy-audit services fund the project after month 12 (EU Cyber Resilience Act deadlines drive demand through Dec 2027).

---

**Checklist before submission**
- [ ] Fill [TODO] (identity + affiliation)
- [ ] 90-second demo video link (public)
- [ ] Link to public repo + first 100 antibodies (public)
- [ ] Confirm eligibility & payment logistics with NLnet (bank transfer to Yemen) — ask early, not after selection
- [ ] Proofread: short, factual, no marketing language
