# RFCs — GERMLINE Requests for Comment

Design documents for the GERMLINE protocol surface. RFCs are numbered, dated,
and versioned; a published RFC is never edited in place — changes arrive as a
new RFC that supersedes it.

| RFC | Title | Status | Date |
|---|---|---|---|
| [RFC-0](0001-abx-antibody-exchange-format.md) | **ABX — Antibody Exchange Format v0.1** | Draft | 2026-10-14 |

## Process (deliberately lightweight at v0)

1. **Draft** — a design problem exists and a concrete proposal is written as an RFC in this folder.
2. **Review** — the proposal is circulated publicly (issue labeled `rfc`, mailing list, or grant reviewers); objections must be answered in writing.
3. **Accepted / Rejected** — the status line is updated with the decision and the deciding rationale.
4. **Superseded** — a later RFC takes over; the old one stays online with a pointer.

Anyone may propose an RFC. The bar is not seniority but *specificity*: a proposal
must state the problem, the design, the rejected alternatives, and the failure modes.

> Why bother at v0? A format that will carry verification evidence across
> organizations must be frozen in public, with its rules written down before
> there is an installed base to please. RFC-0 is the first brick of that
> discipline.
