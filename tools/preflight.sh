#!/usr/bin/env bash
# GERMLINE — preflight: run the exact checks CI will run, before pushing.
#
# Usage:  bash tools/preflight.sh
# Exit:   0 = safe to push · 1 = something CI would reject
set -u
cd "$(dirname "$0")/.." || exit 2

fail=0
step() { printf '\n\033[36;1m▶ %s\033[0m\n' "$1"; }
ok()   { printf '  \033[32m✓ %s\033[0m\n' "$1"; }
bad()  { printf '  \033[31m✗ %s\033[0m\n' "$1"; fail=1; }

step "1/6  Shell scripts carry the executable bit"
missing=0
for f in tools/*.sh corpus/antibodies/*/double-check.sh; do
  [ -x "$f" ] || { bad "not executable: $f"; missing=$((missing+1)); }
done
[ "$missing" = "0" ] && ok "all shipped scripts are executable"

step "2/6  Corpus check (dry-run, no Docker)"
if bash tools/run-corpus-checks.sh --dry-run >/tmp/preflight-dry.log 2>&1; then
  ok "$(grep -o 'total:.*' /tmp/preflight-dry.log | tail -1)"
else
  bad "dry-run failed — see /tmp/preflight-dry.log"; tail -5 /tmp/preflight-dry.log
fi

step "3/6  Web app smoke tests"
if python3 tests/smoke_test.py >/tmp/preflight-smoke.log 2>&1; then
  ok "$(tail -1 /tmp/preflight-smoke.log)"
else
  bad "smoke tests failed — see /tmp/preflight-smoke.log"; tail -5 /tmp/preflight-smoke.log
fi

step "4/6  Prototype immune gate"
if python3 prototype/immune_gate.py >/dev/null 2>&1; then ok "prototype runs"; else bad "prototype failed"; fi

step "5/6  ABX conformance (RFC-0, L2)"
if python3 tools/abx.py validate corpus/abx/*.abx.json >/tmp/preflight-abx.log 2>&1; then
  ok "$(tail -1 /tmp/preflight-abx.log)"
else
  bad "ABX validation failed"; tail -5 /tmp/preflight-abx.log
fi

step "6/6  ABX drift (documents must match their sources)"
if python3 tools/abx.py convert --corpus corpus --out corpus/abx --check >/tmp/preflight-drift.log 2>&1; then
  ok "$(tail -1 /tmp/preflight-drift.log)"
else
  bad "DRIFT — regenerate with: python3 tools/abx.py convert --corpus corpus --out corpus/abx --all"
  grep '✗' /tmp/preflight-drift.log | head -5
fi

printf '\n'
if [ "$fail" = "0" ]; then
  printf '\033[32;1m✅ preflight passed — safe to push\033[0m\n'
else
  printf '\033[31;1m⛔ preflight failed — fix the items above before pushing\033[0m\n'
fi
exit "$fail"
