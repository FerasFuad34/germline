#!/usr/bin/env bash
# AB-000078 — double-check: fail on vulnerable / pass on fixed.
exec bash "$(cd "$(dirname "$0")/../../.." && pwd)/tools/double-check-one.sh" "AB-000078" "$@"
