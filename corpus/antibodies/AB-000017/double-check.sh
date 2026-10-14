#!/usr/bin/env bash
# AB-000017 — double-check: fail on vulnerable / pass on fixed.
exec "$(cd "$(dirname "$0")/../../.." && pwd)/tools/double-check-one.sh" "AB-000017" "$@"
