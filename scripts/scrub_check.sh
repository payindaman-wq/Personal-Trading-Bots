#!/usr/bin/env bash
# scripts/scrub_check.sh — personal-data leak CI guard
#
# Scans tracked files for strings that must not appear in the public template.
# Exit 0 if clean; exit 1 with file:line:match output if violations found.
#
# Allowlist: .scrub_allowlist at repo root — one regex per line, # = comment.
# A finding is suppressed when the "file:line:content" string matches any entry.
#
# TODO (migration day — see docs/migration_runbook.md):
#   1. Add new VPS IP to GLOBAL_PATTERNS below.
#   2. Remove coldstoneadmin ALLOWED comment; add 'coldstoneadmin' to check_pattern calls.
#   3. Audit .scrub_allowlist: remove migration_runbook.md + getting_started.md entries
#      once those files are updated to use YOUR_USERNAME / YOUR_VPS_HOST placeholders.
#   4. Swap allowed handle: replace coldstoneadmin allowance with payindaman-wq.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
ALLOWLIST="${REPO_ROOT}/.scrub_allowlist"
ERRORS=0

# --- Load allowlist ---
ALLOWLIST_PATTERNS=()
if [[ -f "$ALLOWLIST" ]]; then
    while IFS= read -r line; do
        [[ -z "$line" || "${line:0:1}" == "#" ]] && continue
        ALLOWLIST_PATTERNS+=("$line")
    done < "$ALLOWLIST"
fi

is_allowed() {
    local match_line="$1"
    local pat
    for pat in "${ALLOWLIST_PATTERNS[@]+"${ALLOWLIST_PATTERNS[@]}"}"; do
        if echo "$match_line" | grep -qE "$pat" 2>/dev/null; then
            return 0
        fi
    done
    return 1
}

# check_pattern LABEL GREP_REGEX [FILE_FILTER_REGEX]
# FILE_FILTER_REGEX is matched against git ls-files output; omit to scan all tracked files.
check_pattern() {
    local label="$1"
    local grep_regex="$2"
    local file_filter="${3:-}"
    local file_list

    if [[ -n "$file_filter" ]]; then
        file_list=$(git ls-files | grep -E "$file_filter" || true)
    else
        file_list=$(git ls-files)
    fi

    [[ -z "$file_list" ]] && return 0

    local match_line
    while IFS= read -r match_line; do
        [[ -z "$match_line" ]] && continue
        if ! is_allowed "$match_line"; then
            echo "  FAIL [$label]: $match_line"
            ERRORS=$((ERRORS + 1))
        fi
    done < <(echo "$file_list" | tr '\n' '\0' | xargs -0 grep -nE "$grep_regex" 2>/dev/null || true)
}

cd "$REPO_ROOT"

# --- Global patterns: all tracked files ---
check_pattern "VPS_IP"       '204\.168\.167\.19'
check_pattern "GITHUB_PAT"   'ghp_[a-zA-Z0-9]{20,}'
check_pattern "TG_BOT_TOKEN" 'bot[0-9]+:[A-Za-z0-9_-]{30,}'
check_pattern "HANDLE"       'payindaman'

# coldstoneadmin is CURRENTLY ALLOWED — it is the upstream owner for this repo.
# TODO migration: add check_pattern "HANDLE" 'coldstoneadmin' here and remove from allowlist.

# --- Scoped patterns: Norse officer names in config/workflow/setup files only ---
# *.md files legitimately reference officer names throughout (system documentation).
# Scoped to config templates and setup scripts where fork users set their own identity.
# NJORD excluded: it is the framework's capital-allocation config key (config.example.yaml).
# SYN excluded: generic English abbreviation, too many false positives.
check_pattern "NORSE_IN_CONFIG" \
    '\b(ODIN|MIMIR|FREYA|LOKI|TYR|VIDAR|HEIMDALL)\b' \
    '\.(yaml|yml)$|scripts/setup\.sh$'

if [[ $ERRORS -eq 0 ]]; then
    echo "scrub_check: CLEAN (${#ALLOWLIST_PATTERNS[@]} allowlist entries active)"
    exit 0
else
    echo ""
    echo "scrub_check: FAILED — $ERRORS forbidden match(es) found"
    exit 1
fi
