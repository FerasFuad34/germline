#!/usr/bin/env bash
# GERMLINE — corpus-wide double-check runner
#
# Usage:
#   tools/run-corpus-checks.sh --sample 5            # first N antibodies
#   tools/run-corpus-checks.sh --only AB-000001      # one antibody
#   tools/run-corpus-checks.sh --all                 # all (slow: pulls many images)
#   tools/run-corpus-checks.sh --dry-run             # no docker: validate corpus integrity & print plan
#   tools/run-corpus-checks.sh --sample 3 --report out/verification.json
#
# Notes:
#   * docker is required (not for --dry-run)
#   * writes a JSON report with per-antibody verdicts
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CORPUS="$ROOT/corpus/antibodies"

SAMPLE=""; ONLY=""; LIST=""; ALL=0; DRY=0; REPORT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --sample) SAMPLE="$2"; shift ;;
    --only) ONLY="$2"; shift ;;
    --list) LIST="$2"; shift ;;   # comma-separated ids, e.g. AB-000001,AB-000042
    --all) ALL=1 ;;
    --dry-run) DRY=1 ;;
    --report) REPORT="$2"; shift ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

if [ -z "$ONLY" ] && [ -z "$LIST" ] && [ -z "$SAMPLE" ] && [ "$ALL" = "0" ] && [ "$DRY" = "0" ]; then
  echo "choose a scope: --sample N | --only AB-XXXXXX | --list A,B | --all | --dry-run [--sample N]" >&2
  exit 2
fi

list_targets() {
  if [ -n "$ONLY" ]; then echo "$ONLY"; return; fi
  if [ -n "$LIST" ]; then echo "$LIST" | tr ',' '\n'; return; fi
  ls "$CORPUS" | sort
}

targets="$(list_targets)"
if [ -n "$SAMPLE" ]; then targets="$(echo "$targets" | head -n "$SAMPLE")"; fi
if [ "$ALL" = "1" ] && [ -z "$SAMPLE" ] && [ -z "$ONLY" ]; then targets="$(ls "$CORPUS" | sort)"; fi

total=0; ok=0; bad=0; err=0
results="[]"

echo "🧬 GERMLINE corpus check — scope: ${ONLY:-${SAMPLE:-all} $( [ "$DRY" = "1" ] && echo "(dry-run)" )}"
echo "════════════════════════════════════════════════════════"

while IFS= read -r AB; do
  [ -z "$AB" ] && continue
  total=$((total+1))
  DIR="$CORPUS/$AB"

  if [ ! -d "$DIR" ]; then
    err=$((err+1)); printf '  ⚠️  %s missing antibody directory\n' "$AB"
    results="$(echo "$results" | jq --arg ab "$AB" '. + [{antibody:$ab, verdict:"environment-error", detail:"missing directory"}]')"
    continue
  fi

  # integrity checks (always)
  integrity="ok"
  for f in manifest.yaml README.md meta.json double-check.sh; do
    [ -f "$DIR/$f" ] || integrity="missing:$f"
  done
  jq -e . "$DIR/meta.json" >/dev/null 2>&1 || integrity="bad-json"

  if [ "$DRY" = "1" ]; then
    marker="$(jq -r '.detection_marker' "$DIR/meta.json" 2>/dev/null || echo '?')"
    imgv="$(jq -r '.docker.vulnerable' "$DIR/meta.json" 2>/dev/null || echo '?')"
    proj="$(jq -r '.project' "$DIR/meta.json" 2>/dev/null || echo '?')"
    printf '  %s  %-14s %-42s  would run: docker run --rm %s arvo\n' "$AB" "$proj" "$marker" "$imgv"
    if [ "$integrity" = "ok" ]; then ok=$((ok+1)); else bad=$((bad+1)); fi
    results="$(echo "$results" | jq --arg ab "$AB" --arg integ "$integrity" \
      '. + [{antibody:$ab, mode:"dry-run", integrity:$integ}]')"
    continue
  fi

  out="$(bash "$DIR/double-check.sh" --json 2>/dev/null)"
  v="$(echo "$out" | jq -r '.verdict // "error"' 2>/dev/null)"
  case "$v" in
    verified) ok=$((ok+1)); printf '  ✅ %s verified\n' "$AB" ;;
    mismatch) bad=$((bad+1)); printf '  ❌ %s MISMATCH\n' "$AB" ;;
    *)        err=$((err+1)); printf '  ⚠️  %s environment-error\n' "$AB" ;;
  esac
  results="$(echo "$results" | jq --argjson r "${out:-null}" '. + [$r]')"
done <<< "$targets"

echo "════════════════════════════════════════════════════════"
printf '  total: %d | verified: %d | mismatch: %d | errors: %d\n' "$total" "$ok" "$bad" "$err"

if [ -n "$REPORT" ]; then
  mkdir -p "$(dirname "$REPORT")"
  jq -n --argjson results "$results" \
        --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        --argjson t "$total" --argjson ok "$ok" --argjson bad "$bad" --argjson err "$err" \
        '{generated_at:$ts, scope:{total:$t, verified:$ok, mismatch:$bad, errors:$err}, results:$results}' \
        > "$REPORT"
  echo "  report: $REPORT"
fi

[ "$bad" = "0" ] && [ "$err" = "0" ] && exit 0 || exit 1
