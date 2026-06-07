#!/usr/bin/env bash
# Creates the GitHub label set the attended pipeline runs on (CLAUDE.md §7).
# Requires the GitHub CLI (`gh`) authenticated against this repo.
# Re-running is safe: existing labels are updated, not duplicated.

set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install it (https://cli.github.com) or create the labels by hand from the list below." >&2
  exit 0
fi

# name|color|description
labels=(
  "needs-review|fbca04|QA waiting on Aram (exclusive — strip other labels when applied)"
  "qa-pass|0e8a16|Passed QA"
  "qa-improve|d4c5f9|Passed but needs improvement"
  "qa-fail|b60205|Failed QA"
  "spec-ready|0052cc|Spec is ready; build may start"
  "build-session|1d76db|Build session"
  "plan-session|1d76db|Plan session"
  "improve-session|1d76db|Improve session"
  "audit-session|1d76db|Audit session"
  "infra-session|1d76db|Infra / meta session"
  "P1|b60205|Priority 1"
  "P2|fbca04|Priority 2"
  "P3|c2e0c6|Priority 3"
  "blocker|b60205|Blocks other work"
  "dependency|fef2c0|Waiting on a parent issue"
  "bug|d73a4a|Something is broken"
  "epic|3e4b9e|Large multi-issue effort"
  "human-closed|ededed|Closed directly by Aram (owner-approved)"
  "tier:large|5319e7|Full SPEC file + standard QA"
  "tier:small|5319e7|Inline one-paragraph SPEC"
  "tier:tiny|5319e7|Issue body is the SPEC"
  "feedback|0e8a16|External feedback (dormant until a provider is named in CLAUDE.md §3)"
  "feedback:product|c2e0c6|Product feedback (UX, features, output quality)"
  "feedback:business|c5def5|Business feedback (monetization, positioning, growth)"
)

for entry in "${labels[@]}"; do
  IFS='|' read -r name color desc <<< "$entry"
  gh label create "$name" --color "$color" --description "$desc" --force >/dev/null
  echo "label ready: $name"
done

echo "All attended-pipeline labels created."
