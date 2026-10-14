#!/usr/bin/env bash
# AB-000034 — double-check: fail on vulnerable / pass on fixed.
exec "$(cd "$(dirname "$0")/../../.." && pwd)/tools/double-check-one.sh" "AB-000034" "$@"
