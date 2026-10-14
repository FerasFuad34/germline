# 🧬 GERMLINE

**Security inheritance for code generations.**

> SBOM tells you what's *inside* your code. GERMLINE tells you what your code *survived* — and proves the next generation still survives it.

**🚀 Live demo:** **[germline.onrender.com](https://germline.onrender.com)** — run the Immune Gate interactively
**Status:** pre-alpha · building in public · [Roadmap](ROADMAP.md)

---

## The corpus — 100 antibodies · 17 critical projects · 3 verified

`corpus/` holds **100 antibodies** generated from [ARVO](https://github.com/n132/ARVO-Meta) (OSS-Fuzz, EuroS&P 2026):
libxml2 ×14 · ffmpeg ×14 · imagemagick ×12 · harfbuzz ×10 · curl ×8 · wireshark ×7 · ghostpdl ×6 · php-src ×5 · libarchive ×5 · gpac ×4 · binutils-gdb ×4 · freetype2 ×3 · openssl ×3 · libwebp ×2 · zlib, libpng, libtiff ×1 each.
15 crash types · 3 sanitizers (asan/msan/ubsan) · 26 High-severity — each with fix commit, OSS-Fuzz report, Docker reproduction command, and a SHA-256 of the expected crash output.

```bash
bash tools/run-corpus-checks.sh --dry-run     # integrity check, no Docker needed
bash tools/run-corpus-checks.sh --sample 5    # double-check: crash on vul / clean on fix
python3 extractor/arvo.py --help              # regenerate the corpus from arvo.db
```

Status: 🟢 **3/100 verified end-to-end in CI** — AB-000001 … AB-000003 (crash on vulnerable /
clean on fixed; run log in [corpus/VERIFICATION.md](corpus/VERIFICATION.md)) · 🟡 98 draft awaiting the double-check.

Every antibody is also published in **ABX v0.1** — the open exchange format of
[RFC-0](docs/rfc/0001-abx-antibody-exchange-format.md) ([schema](schema/abx-0.1.schema.json),
[validator](tools/abx.py), [100 documents](corpus/abx/)):

```bash
python3 tools/abx.py convert --corpus corpus --out corpus/abx --all   # render the wire format
python3 tools/abx.py validate corpus/abx/*.abx.json                   # schema + invariants (L2)
```

## Demo video (90 s)

[![GERMLINE demo](https://img.shields.io/badge/▶_watch-90s_demo-22d3ee)](https://github.com/FerasFuad34/germline/releases/download/v0.1.0/germline-demo-90s.mp4)

Narrated walkthrough: the problem (immune amnesia), the antibody, the corpus,
ABX/RFC-0, the verification log, and the Immune Gate.

## Dataset v0.1 (citable)

A self-contained, citable package of the corpus — 100 antibody records, the 100
ABX documents, the RFC-0 spec, schema and validator, plus a full datasheet and a
SHA-256 manifest of every file. Deterministic build: the same sources always
produce the same archive bytes.

```bash
python3 tools/build-dataset.py       # -> dist/germline-corpus-v0.1.0.zip (+ .sha256)
```

Download: [**Release v0.1.0**](https://github.com/FerasFuad34/germline/releases) ·
Citation: [CITATION.cff](CITATION.cff) · DOI: Zenodo deposit in preparation
(metadata ready in `dataset/metadata/zenodo-deposit.json`).

## Try it now (live)

```bash
# The immune gate verdict for the demo lineage:
curl https://germline.onrender.com/api/gate?generation=g2   # Rust rewrite → immune parity VERIFIED
curl https://germline.onrender.com/api/gate?generation=g1   # legacy patch  → 3 inherited antibodies FAILED

# Signed Immune Passports (demo signatures):
curl https://germline.onrender.com/passport.json

# Or open the interactive gate in your browser:
open https://germline.onrender.com/demo
```


---

## The problem

Software is being rewritten at an unprecedented rate — whole libraries are translated to memory-safe languages by AI (Google rewrote giflib from C to Rust with AI assistance; DARPA's TRACTOR program is doing this at national scale). Every rewritten generation is a **new body with no immune memory**:

- AI coding assistants reproduce historically vulnerable patterns **~33% of the time** — and *older* vulnerabilities are reproduced more often.
- Vulnerability **reintroduction** is measurable and studied (e.g., 76 reintroduced vulnerabilities found in ImageMagick alone).
- Today, **no tool measures whether a rewritten generation inherited the security protections its ancestor acquired** through years of painful fixes.

Meanwhile, regulation has arrived: since **11 September 2026**, the EU Cyber Resilience Act requires manufacturers to report *actively exploited* vulnerabilities within **24 hours** — applying retroactively to products already on the market.

## What we build

**1. Antibody Corpus** — historical, *fixed*, publicly disclosed vulnerabilities converted into permanently reproducible regression tests ("antibodies"). Each antibody must **fail on the vulnerable version and pass on the fixed version** — no exceptions, verified in CI.

**2. Immune Gate** — a CI/CD gate that, for any artifact (rewrite, fork, translation), replays **all antibodies inherited from its ancestors** and issues a signed **Immune Passport** — portable proof of inherited protection, or a precise report of *immune amnesia*.

**3. ABX (Antibody eXchange)** — an open specification so antibodies travel across tools, vendors, and organizations — never another closed silo.

```
  C library (gen0)          AI rewrite → Rust (gen1)         fork / further gen2
 ┌───────────────┐         ┌──────────────────┐           ┌──────────────────┐
 │ fixes acquired│  ────►  │  INHERITED?      │   ────►   │    INHERITED?    │
 │ over years    │         │  Immune Gate     │           │    Immune Gate   │
 └───────────────┘         └────────┬─────────┘           └────────┬─────────┘
        │                           │                              │
        └──► Antibody Corpus ───────┴────────► signed Immune Passport
```

## Principles (non-negotiable)

1. **Fixed & public only** — we never touch live 0-days; only fixed, publicly disclosed vulnerabilities (ARVO / OSS-Fuzz / CVE).
2. **Reproducible or it doesn't exist** — every claim ships with a command that proves it.
3. **Signed & revocable** — Sigstore signatures, transparency log; antibodies can be revoked if flawed.
4. **Open by default** — code (Apache-2.0), data (CC-BY-4.0), spec (open). The commons stays common.

## Repository layout

| Path | What |
|---|---|
| `corpus/` | The antibody corpus (the heart of the project) |
| `extractor/` | Tooling that mines reproducible vulnerabilities into antibodies |
| `gate/` | The CI/CD Immune Gate + Immune Passport issuer |
| `docs/rfc/` | ABX specification RFCs — [RFC-0](docs/rfc/0001-abx-antibody-exchange-format.md) published |
| `tools/` | Format & verification tooling (`abx.py`, double-check runners) |
| `docs/` | Threat model, sprint plans, and the project's strategic briefs (Arabic) |
| `prototype/` | Early working prototype of the immune gate (demo/simulation) |

## Getting started

Pre-alpha: tooling is landing now. To follow or contribute:

- Read the [Roadmap](ROADMAP.md) — 6 milestones from foundation to company.
- Read `docs/threat-model.md` before proposing corpus changes.
- Want a **free immune audit** of your library's lineage? Open an issue: `type: pilot`.

## Documentation index

- 🇸🇦 الاستراتيجية الكاملة (عربي): `docs/strategic-brief-ar.md`
- ⚙️ نظام التشغيل (عربي): `docs/operating-system-ar.md`
- 🎓 دليل عناوين مشروع التخرج: `docs/graduation-title-guide-ar.md`
- 🗺️ Public roadmap: [ROADMAP.md](ROADMAP.md)
- 📐 RFC-0 — ABX v0.1 (exchange format): `docs/rfc/0001-abx-antibody-exchange-format.md`
- 🛡️ Threat model: `docs/threat-model.md`

## License

Code: **Apache-2.0** · Corpus data: **CC-BY-4.0** · Spec: **open, no patent restrictions**.

*GERMLINE is a working name; naming was validated for package availability (PyPI/npm) and GitHub org availability at project start.*
