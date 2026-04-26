#!/usr/bin/env bash
# Run manually after editing config.yaml. Passphrase prompt is interactive —
# store passphrase in a password manager, NOT on the VPS.
set -euo pipefail

CONFIG="/root/.openclaw/workspace/config.yaml"
BACKUP_DIR="/root/.config-backup"
TODAY="$(date +%Y%m%d)"
DST="${BACKUP_DIR}/config.yaml.${TODAY}.gpg"

mkdir -p "${BACKUP_DIR}"
chmod 700 "${BACKUP_DIR}"

if [ ! -f "${CONFIG}" ]; then
    echo "ERROR: ${CONFIG} not found" >&2
    exit 1
fi

gpg --symmetric --cipher-algo AES256 --output "${DST}" "${CONFIG}"
echo "Backup written to: ${DST}"

ls -t "${BACKUP_DIR}"/config.yaml.*.gpg 2>/dev/null | tail -n +8 | xargs -r rm -f
REMAINING=$(ls "${BACKUP_DIR}"/config.yaml.*.gpg 2>/dev/null | wc -l)
echo "Backups retained: ${REMAINING}"
