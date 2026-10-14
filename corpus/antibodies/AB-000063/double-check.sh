#!/usr/bin/env bash
# AB-000063 — double-check: fail on vulnerable / pass on fixed.
exec bash "$(cd "$(dirname "$0")/../../.." && pwd)/tools/double-check-one.sh" "AB-000063" "$@"
