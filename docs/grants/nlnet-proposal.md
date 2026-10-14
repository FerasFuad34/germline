# NLnet / NGI Zero Commons Fund — Grant Application

### GERMLINE — Immune Inheritance for Software

> **Apply at:** https://nlnet.nl/commonsfund/ — current window closes **3 November 2026**.
> **Requested:** €30,000 over 6 months (first-time applicant range €5k–€50k).
> **Status of this document:** submission-ready except the 4 items listed in the
> checklist at the end (all require personal/banking details).

---

## 1. Abstract (≈170 words)

AI-assisted code rewrites are now routine: critical C/C++ libraries are being
translated to memory-safe languages at scale (Google's AI-assisted giflib→Rust
rewrite; DARPA TRACTOR). Each rewritten generation is a **new body with no immune
memory**: it can silently lose protections its ancestor had already acquired
through years of vulnerability fixes. No tool today measures or enforces the
**inheritance of security protections across code generations**.

GERMLINE builds that missing layer: (1) an **open corpus of executable
"antibodies"** — permanently reproducible tests derived from fixed, publicly
disclosed vulnerabilities (built on ARVO/OSS-Fuzz) — of which **100 are already
published and CI-verified**; (2) an **Immune Gate** for CI/CD that replays all
ancestors' antibodies against any descendant and issues a signed **Immune
Passport**; (3) **ABX** — an open exchange format (**v0.1 spec published**) so
antibodies travel between organizations and vendors. All deliverables are free
and open source, culminating in a benchmark report measuring *immune amnesia* in
real rewrites.

**Already shipped before this grant** (evidence of execution): public repository,
100-antibody corpus v0.1 with double-check verification running in CI, RFC-0
(ABX v0.1) with schema + reference implementation, release v0.1.0.

## 2. Who we are

**[TODO: Full name]**, based in **Aden, Yemen** — independent security engineer
and founder of the GERMLINE project.

- **Background:** [TODO: 2–3 lines — self-taught/degree status, years of
  programming, security focus, notable prior work or coursework.]
- **Track record in this project (verifiable, public):** designed and shipped
  the antibody extractor; published a 100-antibody corpus with an automated
  double-check (crash-on-vulnerable / clean-on-fixed) executed on hosted Docker
  runners; authored RFC-0, the ABX v0.1 exchange format, with a strict JSON
  Schema and a reference validator; built and deployed a live project site.
- **Academic alignment:** [TODO: university + department; this work also serves
  as the graduation project under the working title "Immune Amnesia in
  AI-Assisted Code Rewrites: Measuring the Inheritance of Security Protections
  and a CI/CD Verification Gate".]

## 3. Prior work we build upon (honest positioning)

- **ARVO** (EuroS&P 2026): 6,100+ reproducible vulnerabilities with Docker
  builds, PoC triggers and canonical patches — our antibody source.
- **OSS-Fuzz**: origin of the vulnerability reports referenced by every record.
- **Vul4J / CWE-Bench-Java**: reproducible Java vulnerability benchmarks with
  PoV tests (our stated expansion path).
- **Vulnerability *reintroduction* studies** (ESEM 2022; ImageMagick case study
  2026): measured **within one repository/history**.
  **Gap we address:** nobody measures inheritance **across generations, rewrites
  and languages**, nor provides a portable format that makes such measurements
  comparable between organizations.

## 4. What a reviewer can verify today (links)

| Artifact | Link |
|---|---|
| Repository (Apache-2.0 / CC-BY-4.0) | https://github.com/FerasFuad34/germline |
| Corpus v0.1 release (deterministic archive + SHA-256) | https://github.com/FerasFuad34/germline/releases/tag/v0.1.0 |
| RFC-0 — ABX v0.1 specification | `docs/rfc/0001-abx-antibody-exchange-format.md` |
| Verification log (append-only, per-run evidence) | `corpus/VERIFICATION.md` |
| Datasheet (composition, cleaning, limits) | `dataset/DATASHEET.md` |
| **90-second demo video (public)** | https://github.com/FerasFuad34/germline/releases/download/v0.1.0/germline-demo-90s.mp4 |
| Live demo | https://germline.onrender.com *(free tier; may take ~30 s to wake)* |

## 5. Work packages (6 months)

| WP | Deliverable | Outcome / metric | Effort |
|---|---|---|---|
| **WP1** | **Antibody pipeline at scale**: extend corpus v0.1 (100) → **500+ verified antibodies** across ≥25 projects; automate verification scheduling; publish FP/FN metrics of the acceptance rule. | 500+ antibodies with recorded verification runs; public metrics report | €10,000 |
| **WP2** | **Immune Gate v1**: GitHub Action + CLI; lineage graph (JSON) → replay ancestor antibodies → **signed Immune Passport** (Sigstore + transparency log); 3 OSS pilot integrations. | working Action used by 3 external repos; signed passports | €8,000 |
| **WP3** | **ABX v0.2 + interoperability**: community review round of v0.1 (done pre-grant); v0.2 adds signing profiles, OCI digest pinning, multi-implementation validators (Python + Rust, byte-identical on the conformance corpus); mappings to SPDX/CycloneDX/in-toto/CSAF-VEX. | v0.2 spec + 2 interoperating validators + mapping documents | €6,000 |
| **WP4** | **The Immune Amnesia benchmark report**: measure protection loss across ≥3 real rewrites (including one AI-assisted C→Rust); publish methodology, negative results, replication package with DOI. | public report + Zenodo DOI + reproduction scripts | €4,000 |
| **WP5** | **Community & governance**: threat model, review process, 2 public review rounds, onboarding docs. | documented process + review records | €2,000 |
| | **Total** | | **€30,000** |

## 6. Fit with NGI Zero / the commons

- **Standardization & deployability** — ABX is shared public infrastructure
  (think STIX for threat intel), not a vendor silo; designed to compose with
  SBOM/attestation ecosystems.
- **Security & auditing** — every claim ships with a reproducible check; the
  verification log is append-only and public.
- **Commons-first** — code Apache-2.0, data CC-BY-4.0, specification open, no
  patents, no lock-in; the corpus survives the company if there ever is one.
- **Global South participation** — built and maintained from Yemen, published
  globally: a concrete example of the open internet enabling engineering
  capacity anywhere.

## 7. Risks & mitigation

| Risk | Mitigation |
|---|---|
| False positives in extracted antibodies | Hard acceptance rule (double-check) enforced in CI + published FP metrics (WP1) |
| Corpus poisoning / malicious entries | Signing, review, revocation path, transparency log (WP2/WP3); documented in threat model |
| Scope creep (three deliverables) | One north-star metric: **verified antibodies reused across real projects**; WPs sized to it |
| Solo-founder risk | Public process, documented decisions, RFC review rounds to grow contributors (WP5) |
| Payment logistics from Yemen | Raised with NLnet **before applying** (see checklist) to agree on a workable payout route |

## 8. Budget notes

Individual grant, 6 months, part-time-plus effort (20–30 h/week). The budget
covers engineering time only. Infrastructure stays under €100/month (free/open
CI tiers, object storage, domain) and is **not** requested from NLnet.
All amounts are labor, no hardware, no travel requested.

## 9. Sustainability beyond the grant

Open-core: the standard and corpus remain open forever. After month 12, revenue
comes from (a) a hosted antibody registry with SLA, (b) CRA-compliance reporting
(the EU Cyber Resilience Act's reporting duties are live and its SBOM/conformity
regime lands Dec 2027, driving demand), (c) paid lineage security audits for
companies rewriting legacy code. The grant buys the credibility layer: a
verified corpus, a frozen format, and published measurements.

---

**Checklist before submission**
- [ ] Fill the 3 `[TODO]` identity fields (name, background, university) — 10 minutes
- [x] Public repo + 100 antibodies + CI verification — done
- [x] ABX v0.1 spec + schema + reference implementation — done
- [x] 90-second demo video — recorded, narrated, published: https://github.com/FerasFuad34/germline/releases/download/v0.1.0/germline-demo-90s.mp4
- [ ] Zenodo DOI for corpus v0.1 (owner action, steps documented) — link it in §4 when minted
- [ ] Confirm eligibility & payment logistics with NLnet (bank transfer to Yemen) — **email drafted, send early**
- [ ] Re-verify the live demo link is up before submitting (§4)
- [x] Proofread pass: factual, no marketing language
