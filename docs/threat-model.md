# Threat Model — GERMLINE (draft v0.1)

*Scope: the GERMLINE system itself. This document is a living draft; changes require review (see CONTRIBUTING.md).*

## Assets (what an attacker would want)

| # | Asset | Why it matters |
|---|---|---|
| A1 | **Antibody corpus integrity** | A poisoned antibody could create false immunity claims ("passes" while the artifact is actually vulnerable) or false alarms that destroy trust |
| A2 | **Immune Passport integrity** | A forged passport misrepresents the security state of a real artifact |
| A3 | **Registry availability** | Gates blocking CI across many orgs = supply-chain-scale DoS |
| A4 | **Upstream ARVO/OSS-Fuzz provenance links** | Broken provenance invalidates the corpus's legal/ethical grounding |
| A5 | **Project tooling supply chain** (extractor, gate, CI) | Classic: compromise the security tool, inherit its trust |

*Non-asset by design: working exploits for live systems — GERMLINE only stores tests for fixed, public vulnerabilities.*

## Threat actors

1. **Opportunistic attackers** — scrape, deface, DoS.
2. **Supply-chain adversaries** — inject a poisoned antibody release to weaken downstream consumers.
3. **Insiders / contributors** — well-meant bad antibody (quality), or malicious masquerade (rare but decisive).
4. **Competitors** — cloning the corpus (accepted: it's CC-BY; our moat is trust + lineage data + standard, not secrecy).
5. **PR-driven adversaries** — social-engineer maintainers into merging a subtly wrong binary test (e.g., input that crashes both revisions, rejected by CI double-check by design).

## Key threats & mitigations (STRIDE-flavored)

| ID | Threat | Mitigation (status) |
|---|---|---|
| T1 | **Corpus poisoning** — an antibody is not semantically what it claims | Mandatory CI double-check (fails-on-vul/passes-on-fix) + human review + provenance field + `status: disputed` workflow + revocation. *(double-check: planned M0; revocation: M1)* |
| T2 | **Passport forgery** — fake "immune parity" proof | Sigstore-keyless signing + transparency log; verifiers MUST check log inclusion, not just a signature blob. *(M1)* |
| T3 | **Replay/substitution** — old passport attached to new artifact | Passport covers artifact hash + generation ID; verifier recomputes. *(M1)* |
| T4 | **Tooling compromise** — malicious dependency in extractor/gate | Minimal dependency policy, lockfiles, reproducible builds, signed releases, our own SBOM (dogfooding). *(continuous)* |
| T5 | **Registry DoS / takedown** | Static, cacheable artifacts; gate works fully offline with a pinned corpus snapshot; mirror-friendly layout. *(design constraint from M0)* |
| T6 | **False negatives at scale** — "immune" systems that are actually vulnerable because the antibody corpus is incomplete | Never claim coverage beyond the corpus: passports state `antibodies_inherited` count and explicitly disclaim completeness. Anti-marketing rule: we sell *inheritance*, not *immunity from everything*. |
| T7 | **Ethical/legal drift** — someone upstreams a live 0-day into the corpus | Automated policy check against disclosure status in CI (fixed + public flags required). *(M0)* |
| T8 | **Maintainer-key compromise** | Keyless signing bound to CI identity (OIDC), short-lived credentials, 2-reviewer rule for corpus-wide ops. *(M1)* |

## Explicit non-goals (to prevent scope creep)

- Not an antivirus, EDR, or runtime protection system.
- Not a vulnerability scanner; we assume the vulnerability is already known and fixed.
- Not a patch distributor: **GERMLINE issues tests, evidence, and verdicts — never executable fixes to third-party systems.** (This is a deliberate design response to the failure mode of "auto-patching worms": we avoid distributing executable changes entirely.)

## Open questions (tracked)

1. Privacy of private-lineage graphs (organizations may not want lineage disclosed) → registry design must support private DAGs + public attestations only. *(M4)*
2. Incentives for third-party antibody contributions (recognition first; tokenization rejected on principle). *(M5)*
3. Formal semantics of "inherited": is function-level similarity sufficient, or must lineage be declared? → RFC-0 discussion. *(M0)*
