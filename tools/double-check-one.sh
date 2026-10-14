#!/usr/bin/env bash
# GERMLINE — double-check one antibody (the canonical validation)
#
# Usage:
#   tools/double-check-one.sh AB-000001 [--json] [--timeout 600]
#
# Verdicts:
#   verified            vulnerable crashes with the expected marker AND fixed stays clean
#   mismatch            anything else (records detail)  -> antibody must be fixed or revoked
#   environment-error   docker missing / image pull failed
#
# Exit codes: 0 verified · 1 mismatch · 2 environment error
set -u

AB="${1:-}"; shift || true
JSON=0; TIMEOUT=600
while [ $# -gt 0 ]; do
  case "$1" in
    --json) JSON=1 ;;
    --timeout) TIMEOUT="$2"; shift ;;
  esac
  shift
done

if [ -z "$AB" ]; then echo "usage: double-check-one.sh AB-XXXXXX [--json]" >&2; exit 2; fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="$ROOT/corpus/antibodies/$AB"
META="$DIR/meta.json"

if [ ! -f "$META" ]; then echo "no such antibody: $AB ($META)" >&2; exit 2; fi
if ! command -v docker >/dev/null 2>&1; then
  echo "environment-error: docker not found" >&2; exit 2
fi

IMG_VUL="$(jq -r '.docker.vulnerable' "$META")"
IMG_FIX="$(jq -r '.docker.fixed' "$META")"
MARKER="$(jq -r '.detection_marker' "$META")"

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

run_one() { # $1=image $2=outfile
  timeout "$TIMEOUT" docker run --rm "$1" arvo >"$2" 2>&1
  echo $?
}

verdict=environment-error; detail=""
code_vul=1; code_fix=1; hit_vul=0; hit_fix=0

code_vul="$(run_one "$IMG_VUL" "$work/vul.log")"; rc=$?
if [ "$rc" = "2" ]; then
  detail="environment-error: docker run failed for $IMG_VUL (pull/daemon issue)"
elif [ "$rc" != "0" ]; then
  code_vul="$(run_one "$IMG_VUL" "$work/vul.log")"
fi
grep -qF -- "$MARKER" "$work/vul.log" && hit_vul=1

code_fix="$(run_one "$IMG_FIX" "$work/fix.log")"
grep -qF -- "$MARKER" "$work/fix.log" && hit_fix=1

if [ "$hit_vul" = "1" ] && [ "$hit_fix" = "0" ]; then
  verdict="verified"
elif [ "$hit_vul" = "1" ] && [ "$hit_fix" = "1" ]; then
  verdict="mismatch"; detail="marker also present on fixed build"
elif [ "$hit_vul" = "0" ]; then
  verdict="mismatch"; detail="expected marker not found on vulnerable build"
fi

if [ "$JSON" = "1" ]; then
  jq -n --arg ab "$AB" --arg v "$verdict" --arg d "$detail" \
        --arg m "$MARKER" --arg cv "$code_vul" --arg cf "$code_fix" \
        '{antibody:$ab, verdict:$v, detail:$d, marker:$m,
          vulnerable:{exit:$cv, marker_found:($cv|tonumber? // 0)},
          fixed:{exit:$cf}}' \
  | jq --argjson hv "$hit_vul" --argjson hf "$hit_fix" \
       '.vulnerable.marker_found=$hv | .fixed.marker_found=$hf'
else
  printf '%s\n' "── $AB ─────────────────────────────────────────" \
    "image(vul): $IMG_VUL  → exit=$code_vul marker_found=$hit_vul" \
    "image(fix): $IMG_FIX  → exit=$code_fix marker_found=$hit_fix" \
    "marker:     $MARKER" \
    "verdict:    $verdict ${detail:+($detail)}"
fi

case "$verdict" in
  verified) exit 0 ;;
  mismatch) exit 1 ;;
  *) exit 2 ;;
esac
