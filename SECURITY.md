# Security Policy

## Reporting a vulnerability

**In scope:** the GERMLINE tooling itself — `extractor/`, `gate/`, `corpus/` metadata handling, and the registry (when it exists). This includes: code execution in our tools, signature/verification bypasses, corpus poisoning vectors, and supply-chain issues in our own releases.

**Out of scope:** vulnerabilities in third-party software referenced by the corpus. We only store tests for **already fixed, publicly disclosed** vulnerabilities; we do not exploit live systems and we do not maintain 0-days.

### How to report

- Preferred: **GitHub private vulnerability reporting** (Security tab → "Report a vulnerability").
- Email: `security@[project-domain]` (to be provisioned before public launch — until then, use GitHub private reporting).

### What to expect

| Stage | Timeline |
|---|---|
| Acknowledgment | within 72 hours |
| Initial assessment | within 7 days |
| Fix or mitigation plan | within 30 days for confirmed issues |
| Public disclosure | coordinated, after a fix is available |

### Safe harbor

We will not pursue legal action against researchers who act in good faith: test only against your own deployments of our software, avoid privacy violations and destructive actions, and give us reasonable time to fix before disclosure.

### Corpus integrity reports

If you believe an antibody is incorrect (e.g., it does not actually distinguish vulnerable from fixed builds), open a normal issue with the `type: antibody` and `status: disputed` labels — corpus accuracy is a security property for us, not a nitpick.
