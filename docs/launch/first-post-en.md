# Your AI rewrite passes the tests. Does it still resist the old attacks?

*(First public post — ready to publish on dev.to / Hacker News / GitHub Discussions.
Publish under your own account; the text is complete as-is.)*

---

Software is being rewritten faster than its security memory can survive.

Google rewrote giflib from C to Rust with AI assistance. That project ran 30
million regression tests and 200 million differential-fuzzing iterations — the
gold standard of care. Most rewrites get far less. And even that process cannot
answer a different question: **does the new code still resist every input that
once crashed the old code?**

That question has a name now: **immune amnesia** — the silent loss of security
protections during a rewrite. Studies on vulnerability *reintroduction* (ESEM
2022; a 2026 ImageMagick case study) measure this **within one repository's
history**. What nobody provides is a portable, executable way to measure it
**across generations, rewrites, and languages** — and to run it in CI.

So we built one, and published everything.

## What exists today (all public, all verifiable)

**1. A corpus of antibodies.**
An *antibody* is one historical vulnerability reduced to a discriminating
experiment: a pinned environment that **must fail** (crash + sanitizer marker)
and one that **must stay clean**. No discrimination → not an antibody. There
are **100** of them today, across **17 critical C/C++ projects** (libxml2, ffmpeg,
ImageMagick, harfbuzz, curl, wireshark, OpenSSL…), derived from ARVO's
curation of OSS-Fuzz reports — every record links its public report, fix commit,
and a SHA-256 of the expected crash output.

**2. A verification rule, enforced in CI, with an append-only public log.**
Every recorded result is a real execution on a real container: *crash on the
vulnerable image, clean on the fixed image*. Three antibodies are verified
end-to-end so far (one reproduced across independent runs). The other 97
records say `draft` in plain text — because **absence of verification must
never be rendered as success**. The log lives in the repository; the runner is
open source.

**3. An exchange format: ABX v0.1 (RFC-0).**
Antibodies are useless as screenshots. [RFC-0](https://github.com/FerasFuad34/germline/blob/main/docs/rfc/0001-abx-antibody-exchange-format.md)
defines a strict, canonical, signable JSON document — the experiment, its
expected observations, its evidence, and its verification history. Unknown
fields are rejected on purpose; in a security format, silent drift is a
vulnerability class of its own. There's a strict JSON Schema, a reference
validator (`convert` / `validate` / `digest`), and the corpus ships in both
formats — one source of truth, reconciled by a drift check in CI.

**4. A datasheet and a deterministic release.**
The [v0.1.0 release](https://github.com/FerasFuad34/germline/releases/tag/v0.1.0)
is a self-contained archive: same sources → same bytes, with a SHA-256 manifest
of every file. The [datasheet](https://github.com/FerasFuad34/germline/blob/main/dataset/DATASHEET.md)
documents composition, the three real data defects we found and cleaned while
building the format (multi-commit fix fields, ANSI escapes, multi-line fuzz
targets), and exactly what "draft" means.

## What this is NOT (yet)

- Not a scanner, not a CVE database, not a silver bullet.
- Only 3/100 antibodies are verified; the rest are honestly marked draft.
- The **Immune Gate** — replaying ancestors' antibodies in a pipeline and issuing
  a signed passport — is the next milestone, not a finished product.
- Memory-safety C/C++ first; other classes and languages come after the pipeline
  proves itself.

## Where this is going

Field: **immune inheritance** for software. Ten-year view: a rewrite (human or
AI, any language) should automatically inherit the immune memory of its
ancestors, with a signed record of what was verified — the other half of what an
SBOM promises, and increasingly what the EU Cyber Resilience Act's evidence
culture will demand.

Next steps, in order: the Immune Gate GitHub Action, 500+ verified antibodies,
and a benchmark report measuring immune amnesia in a real AI-assisted C→Rust
rewrite — including negative results.

## How you can help (10 minutes each)

1. **Read RFC-0 and try to break it.** Counterexamples are exactly what a
   format needs before it has an installed base.
2. **Run the validator** on the corpus and tell us what fails:
   `python3 tools/abx.py validate corpus/abx/*.abx.json`
3. **Pilot a lineage:** if your project has a rewrite (or a fork that diverged
   years ago), open an issue — we're looking for 3 pilot repositories.
4. **Signal:** a star/fork helps most when you also dislike something specific —
   tell us what.

**Repository:** https://github.com/FerasFuad34/germline
**Release v0.1.0:** https://github.com/FerasFuad34/germline/releases/tag/v0.1.0
**Live demo:** https://germline.onrender.com *(free tier: may take ~30 s to wake)*

*Building this from Aden, Yemen — an independent effort, applying to the NLnet
NGI Zero Commons Fund to fund the next six months of work. Feedback of any kind
is fuel.*

---

## Publishing checklist

- [ ] Post on dev.to (canonical link → the repository)
- [ ] Show HN: title "Show HN: GERMLINE – 100 executable antibodies to catch security loss in AI rewrites"
- [ ] Link in `README.md` ("In the press / community" section) after publishing
- [ ] Cross-post the Arabic summary on LinkedIn/local networks
