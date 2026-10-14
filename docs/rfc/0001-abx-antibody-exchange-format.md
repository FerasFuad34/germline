# RFC-0 — ABX: Antibody Exchange Format v0.1

| | |
|---|---|
| **Document** | RFC-0 |
| **Version** | 0.1 (draft) |
| **Date** | 2026-10-14 |
| **Status** | Draft — open for public review |
| **Editor** | GERMLINE project |
| **License** | Apache-2.0 (this document) · CC-BY-4.0 (upstream data references) |
| **Schema** | [`schema/abx-0.1.schema.json`](../../schema/abx-0.1.schema.json) |
| **Reference implementation** | [`tools/abx.py`](../../tools/abx.py) |
| **Conformance corpus** | [`corpus/abx/`](../../corpus/abx/) (100 generated documents) |

---

## 1. Abstract

**ABX** is a small, strict, machine-readable format for exchanging *antibodies*:
executable security checks that encode a historical vulnerability together with
the experiment that proves a given build still resists it.

An ABX document does not describe a vulnerability in prose. It specifies a
**discriminating experiment**: one environment that must fail, one that must
stay clean, and the evidence that this discrimination has actually been observed.
The unit of value in ABX is not the finding — it is *the difference between two states*.

ABX is deliberately tiny, canonicalizable, and free of executable payloads.
It is designed to be referenced from OSV records, attached to release artifacts,
carried across AI-assisted code rewrites, and verified by third parties who
distrust the publisher.

## 2. Motivation

Three shifts make a shared format for *reusable security verification* necessary now:

1. **AI rewrites code faster than security knowledge survives.** Rewrites from C to
   Rust (or any language hop) routinely drop security properties that were never
   written down as tests. A rewritten module that compiles, passes its old test
   suite, and still accepts an input that once crashed the original is a
   *regression*, but no artifact in the pipeline says so.
2. **Regulation now demands evidence, not intentions.** The EU CRA's reporting
   duties are live, and its SBOM + conformity-assessment duties arrive in Dec 2027.
   An SBOM names ingredients; an ABX document states *what was proven about them* —
   the missing half of supply-chain transparency.
3. **Disclosure artefacts are not reusable.** A CVE record, a patch, a fuzzing
   crash log and a GitHub issue each hold one fragment. Nothing standard binds
   them into "this build is immune, and here is the test that proves it."

ABX is the smallest format that closes that loop. It composes with existing
standards (OSV, CVE, CWE, SARIF, VEX, in-toto, SLSA) instead of replacing any of them.

### 2.1 Non-goals

- **Not a vulnerability database.** ABX references OSV/CVE identifiers; it does not
  attempt to be one.
- **Not a scanner output.** SARIF reports what a tool *observed*; ABX states what
  *must* be observed to accept a build.
- **Not a PoC distribution channel.** No exploit payloads, no binaries, no seeds —
  only digests, references and short fair-use excerpts (§6, INV-4).
- **Not a scoring system.** Severity is carried, not computed.

## 3. Terminology

| Term | Meaning in this document |
|---|---|
| **Antibody** | A persistent, executable check derived from a fixed, publicly disclosed vulnerability; replaying it must distinguish a vulnerable state from a fixed state. |
| **Subject** | The project/component a challenge concerns. |
| **Challenge** | The experiment: harness, target, expected observation on each side. |
| **Discrimination** | The property that a challenge fails on the vulnerable side *and* passes on the fixed side. An antibody without discrimination has zero value (INV-1). |
| **Verdict** | Outcome of executing a challenge on a real runner: `verified`, `mismatch`, `environment-error`. |
| **Generation** | A lineage state of a codebase (e.g. `g0` = original C, `g2` = Rust rewrite). |
| **Antigen** | The specific faulty pattern the antibody binds to (crash type + target). |

The immune metaphor is a naming convention, not an implementation requirement;
ABX is fully usable by implementations that ignore the vocabulary.

## 4. Design principles

1. **Data, never code.** An ABX parser must never need to execute anything to read
   an antibody. Execution is confined to the referenced environments, explicitly.
2. **Discrimination or nothing.** A document that cannot point to a measured
   difference between a failing and a passing state is not an antibody (INV-1).
3. **Evidence by reference + digest.** Large artefacts (crash logs, PoCs, patches)
   are referenced by URL and bound by SHA-256. Documents stay small and diffable.
4. **Append-only verification.** Verdicts are historical facts. Corrections are new
   runs, never edits (INV-5).
5. **Strict parsing.** Unknown fields are rejected, not ignored: silent drift in a
   security format is a vulnerability class of its own (§12).
6. **Deterministic rendering.** Two implementations given the same inputs must
   produce byte-identical documents (§7).

## 5. Document structure

An ABX v0.1 document is a JSON object with eleven top-level members.

| Field | Required | Type | Purpose |
|---|---|---|---|
| `abx_version` | ✅ | const `"0.1"` | Format version (semver, §12). |
| `kind` | ✅ | const `"antibody"` | Document type discriminator. |
| `id` | ✅ | `^AB-[0-9]{6}$` | Immutable, globally unique, never reused (INV-2). |
| `title` | ✅ | string 8–180 | Human-readable one-liner. |
| `subject` | ✅ | object | Project, upstream, language, generation, fixed-in ref. |
| `vulnerability` | ✅ | object | Identifiers (CVE/CWE/OSS-Fuzz), class, crash type, sanitizer, severity. |
| `challenge` | ✅ | object | Kind, harness, target, expectation, detector. |
| `environments` | ✅ | object | The two sides that must disagree: `vulnerable`, `fixed`. |
| `evidence` | ✅ | object | Report/patch URLs, fix commit, crash digest, ≤512-char excerpt. |
| `provenance` | ✅ | object | Source dataset + record, generator, timestamp, license. |
| `status` | ✅ | enum | `draft` \| `validated` \| `revoked`. |
| `verification` | conditional | object | Required when `status = validated`; holds append-only runs. |
| `integrity` | ✅ | object | SHA-256 over the canonical body (§7). |
| `signatures` | optional | array | Detached signatures (v0.2 target: Ed25519/sigstore). |
| `ext` | optional | object | Namespaced extension point; the *only* place non-standard fields may live. |

### 5.1 Complete example

```json
{
  "abx_version": "0.1",
  "kind": "antibody",
  "id": "AB-000001",
  "title": "libxml2: Use-of-uninitialized-value in libxml2_xml_read_memory_fuzzer",
  "subject": {
    "project": "libxml2",
    "upstream": "https://gitlab.gnome.org/GNOME/libxml2.git",
    "language": "c++",
    "generation": "g0",
    "fixed_in": "074180119fc9"
  },
  "vulnerability": {
    "identifiers": { "cve": [], "cwe": ["CWE-457"], "oss_fuzz": "42470114" },
    "class": "memory-safety",
    "crash_type": "Use-of-uninitialized-value",
    "sanitizer": "msan",
    "severity": "Medium",
    "cvss": null
  },
  "challenge": {
    "kind": "proof-of-vulnerability",
    "harness": "docker run --rm n132/arvo:42470114-vul arvo",
    "target": "libxml2_xml_read_memory_fuzzer",
    "expect": { "vulnerable": "crash", "fixed": "clean" },
    "detector": { "type": "stdout-regex", "match": "WARNING: MemorySanitizer" }
  },
  "environments": {
    "vulnerable": { "type": "oci-image", "ref": "n132/arvo:42470114-vul" },
    "fixed": { "type": "oci-image", "ref": "n132/arvo:42470114-fix" }
  },
  "evidence": {
    "report": "https://issues.oss-fuzz.com/issues/42470114",
    "patch": "https://gitlab.gnome.org/GNOME/libxml2/-/commit/074180119fc90d5fd04ef9e8a5ee1910d6f9ad8e",
    "fix_commit": "074180119fc90d5fd04ef9e8a5ee1910d6f9ad8e",
    "crash_digest": { "alg": "sha256", "value": "25f02061c96b3888255fb8e9160fa132724b3b771aba978eba911bb2f1ba69c9" },
    "crash_excerpt": "WARNING: MemorySanitizer: use-of-uninitialized-value ... xmlParserPrintFileContextInternal /src/libxml2/error.c:201"
  },
  "provenance": {
    "source": { "dataset": "ARVO", "version": "v3.0.0", "record": "42470114" },
    "generated_by": "germline-extractor/0.1",
    "generated_at": "2026-10-14T20:12:39Z",
    "license": "Apache-2.0 (document) / CC-BY-4.0 (upstream data)"
  },
  "status": "validated",
  "verification": {
    "last_verdict": "verified",
    "runs": [
      {
        "runner": "github-actions/ubuntu-latest",
        "run_id": "38630272283",
        "run_url": "https://github.com/FerasFuad34/germline/actions/runs/38630272283",
        "date": "2026-10-14",
        "observed": { "vulnerable": "crash", "fixed": "clean" },
        "verdict": "verified"
      }
    ]
  },
  "integrity": { "algorithm": "sha256", "value": "<digest of canonical body>" }
}
```

## 6. Semantics and invariants

These are normative. A document violating any of them is **invalid** even if it
passes the JSON Schema (which can only express a subset).

- **INV-1 — Discrimination is mandatory.** `challenge.expect.vulnerable` ≠
  `challenge.expect.fixed`; the fixed side must be `clean`, and the vulnerable
  side must be one of `crash`, `error`, `timeout`, `misbehavior`.
  A challenge whose two sides are expected to behave identically is not an antibody.
- **INV-2 — IDs are permanent.** `id` values are never reused, never renumbered,
  and never reassigned to a different subject. Retirement = `status: revoked`.
- **INV-3 — Environments are explicit and pinned.** Both sides must name a
  resolvable reference: an OCI image, a `source-commit`, or a lineage `generation`.
  Floating tags (`:latest`) are invalid.
- **INV-4 — No payloads.** Documents must not embed binaries, base64 blobs, exploit
  code, fuzzing seeds, or personal data. Evidence is by reference + digest;
  `crash_excerpt` is capped at 512 characters.
- **INV-5 — Verification is append-only.** `verification.runs` may only grow.
  A recorded `verdict` is immutable; later contradicting observations are *new*
  runs. `revoked` requires a run entry stating why.
- **INV-6 — Status ≠ claim.** `status: validated` requires at least one run with
  `verdict: verified`. Absence of verification must never be rendered as success.
- **INV-7 — Provenance is checkable.** `provenance.source` must name the dataset
  and the exact record within it; the originating issue and patch must be public
  and fixed (no undisclosed vulnerabilities — see §11.4).
- **INV-8 — Detectors are positive.** A detector states what *failure* looks like
  (marker/code), never what success looks like; this prevents vacuously passing
  checks (e.g., a harness that never ran).
- **INV-9 — Integrity covers content.** `integrity.value` must equal the SHA-256
  of the canonical body (§7). Documents with a mismatching digest are rejected.

## 7. Canonicalization and integrity

1. The **body** is the document with `integrity` and `signatures` removed.
2. Canonical form: JSON with keys sorted lexicographically, no insigificant
   whitespace, UTF-8, numbers in the restricted form defined by RFC 8785 (JCS);
   v0.1 documents contain no floating-point values other than `null`/integers,
   so the profile is trivially conformant.
3. `integrity.value = sha256_hex(canonical(body))`.
4. `signatures[]` (optional in v0.1) sign the *canonical body*. v0.1 defines the
   container, not the algorithms; interoperable signature methods (Ed25519 key
   files, sigstore bundles) are the v0.2 deliverable.

Tooling: `python3 tools/abx.py digest <file>` recomputes and verifies.

## 8. Verification protocol

Executing a challenge — the "double-check" — is the operation that turns a draft
document into a verified one. The protocol is normative for anyone claiming ABX
conformance of a verdict.

| Step | Action | Failure mode it excludes |
|---|---|---|
| VP-1 | **Fetch** both environments from their pinned references. | Building from moving branches. |
| VP-2 | **Run the vulnerable side**; capture stdout/stderr/exit code. | Claiming a crash that no longer reproduces. |
| VP-3 | **Assert failure**: detector matches, and the observation equals `expect.vulnerable`. | Vacuously passing harnesses. |
| VP-4 | **Run the fixed side**; assert it produces `expect.fixed` (`clean`, i.e. detector does *not* match). | Fix not actually landed / patch incomplete. |
| VP-5 | **Record** runner identity, run id/URL, date, both observations, verdict. | Unattributable claims. |
| VP-6 | **Append** the run; promote `draft → validated` only on `verified`; keep mismatches visible. | Cherry-picking runs. |

Verdict vocabulary (closed set):

| Verdict | Meaning |
|---|---|
| `verified` | VP-3 and VP-4 both held. |
| `mismatch` | The environment did not behave as the document claims (either side). |
| `environment-error` | Infrastructure failure (pull error, timeout of the runner, missing tool). Never counts as success. |

## 9. Conformance levels

| Level | Requirement | Test |
|---|---|---|
| **L1 — Well-formed** | Validates against `schema/abx-0.1.schema.json`. | `tools/abx.py validate --level 1` |
| **L2 — Semantically valid** | L1 + all invariants INV-1…INV-9 hold. | `tools/abx.py validate` (default) |
| **L3 — Verified** | L2 + ≥1 appended run with `verdict: verified`. | `tools/abx.py validate --level 3` |

Publishers SHOULD state the level they claim. Consumers MUST NOT treat an L1/L2
document as evidence of anything except well-formedness.

## 10. Relationship to other standards

ABX is a composition layer. It does not compete with any of these:

| Standard | What it provides | What ABX adds |
|---|---|---|
| OSV / CVE | Identity of a disclosed vulnerability | The *experiment* that proves a build resists it |
| CWE | Weakness taxonomy | `vulnerability.cwe` as pointers; ABX never re-taxonomizes |
| SARIF | Static-analysis findings | Actionable acceptance criteria (fail/pass states) |
| VEX / CSAF | Exploitability status of a product | A measured, re-runnable discrimination, not a status assertion |
| in-toto / SLSA | Build provenance & attestations | The subject matter that gets attested (what was verified) |
| CycloneDX / SPDX (SBOM) | Ingredients | Behavioural evidence about those ingredients |

Intended composition: an SBOM names ingredients → an OSV record names a
vulnerability → an ABX document supplies the test and its verification history →
attestations (SLSA/in-toto) bind all three to an artifact.

## 11. Security considerations

1. **Antibodies are code execution instructions.** An `environments` reference
   points at an image that will be run. Consumers MUST treat ABX documents as
   untrusted input: sandboxed execution, no network by default, resource caps
   (CPU/memory/time), no host mounts, non-privileged containers.
2. **Egress-storm / cost DoS.** Automatic replay of many antibodies can burn
   runner minutes. Runners SHOULD cap concurrency and total per-run budget;
   `verification.runs` records observed durations.
3. **Supply-chain trust.** A hostile antibody could reference a malicious image.
   Mitigations: strict `ref` pinning (INV-3), digest-pinned OCI refs encouraged
   in v0.2, signature verification (v0.2), and never auto-executing freshly
   received documents in privileged CI.
4. **Disclosure ethics.** ABX only carries *fixed, publicly disclosed*
   vulnerabilities: no zero-days, no embargoed research, no 0-day PoCs
   (INV-7). The `evidence.report` field makes this auditable.
5. **Vacuously passing checks.** The classic failure of security testing is a
   green light that never actually ran. INV-8 (positive detectors) plus VP-3/VP-4
   (asymmetric expectations) exist specifically to make vacuous success impossible
   to express.
6. **Privacy.** No personal data in documents; crash excerpts are machine output,
   and are capped and required to be attributable to a public report.

## 12. Versioning and compatibility

- `abx_version` is `MAJOR.MINOR`.
- Consumers MUST reject unknown **major** versions; MUST warn on unknown
  **minor** versions; MUST reject unknown fields (strict parsing, principle 5).
- Extensions live under `ext` with reverse-DNS keys (e.g. `ext["sh.germline"]`).
- Deprecations: a field may be marked deprecated by a new minor version; removal
  requires a major bump.
- The JSON Schema file is versioned alongside: `schema/abx-<major>.<minor>.schema.json`.

## 13. Rejected alternatives

| Alternative | Why rejected |
|---|---|
| **YAML + shell scripts** (our internal authoring format) | Ideal for humans, hostile to machines: no canonical form, comment/ordering ambiguity, no signing story. ABX keeps YAML for authoring; `tools/abx.py convert` renders the wire format. |
| **Just use OSV** | OSV answers "which vulnerability is this?" — ABX answers "how do I prove this build resists it, and who verified that?" Complementary, not competing. |
| **Just use SARIF** | SARIF carries findings from scanners; it has no vocabulary for acceptance (fail-vs-pass) states or verification runs. |
| **VEX only** | VEX asserts exploitability status; an assertion is not a measurement. ABX records the measurement and can feed a VEX statement. |
| **Embed the PoC in the document** | Turns a data format into a malware distribution channel and destroys auditability of the payload's origin. Digests + references preserve trust boundaries (INV-4). |
| **Allow unknown fields (lenient parsing)** | Silent schema drift in a security format recreates the "green light that means nothing" failure. Orgs that need extensions have `ext`. |

## 14. Reference implementation

```bash
# render the wire format from the authoring corpus
python3 tools/abx.py convert --corpus corpus --out corpus/abx --all

# validate (L2): schema + invariants, corpus-wide uniqueness
python3 tools/abx.py validate corpus/abx/*.abx.json

# recompute the integrity digest of one document
python3 tools/abx.py digest corpus/abx/AB-000001.abx.json
```

The 100 documents in [`corpus/abx/`](../../corpus/abx/) are generated from the same
ARVO-derived corpus as the internal manifests — two formats, one source of truth,
reconcilable at any time by re-running the converter (`--check` fails on drift).

## 15. Open questions (toward v0.2)

1. **Signature algorithm profile** — Ed25519 raw key files vs sigstore keyless?
2. **OCI digest pinning** — make `environments.*.digest` mandatory (breaks convenience, buys immutability).
3. **Multi-side challenges** — differential testing between two *implementations*
   (e.g. C reference vs Rust rewrite) rather than vulnerable-vs-fixed pairs.
4. **Expiry semantics** — should a verified antibody ever expire? (Proposal: no;
   it records history. Consumers infer staleness from the newest run date.)
5. **Language bindings** — ship a Rust and a Python validator that agree byte-for-byte on the conformance corpus.

---

*RFC-0 is published for public review. Objections, counterexamples, and
counter-proposals are welcome as issues tagged `rfc`.*
