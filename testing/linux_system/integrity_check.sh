#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
for file in /etc/passwd /etc/group /etc/hosts /etc/fstab /etc/sudoers; do
    if [ -f "$file" ]; then
        stat -c '%a %U %n' "$file"
        sha256sum "$file"
        mode=$(stat -c '%a' "$file")
        if (( (8#$mode & 2) != 0 )); then echo "WARN: world-writable $file"; fi
    fi
done
if [ -n "${QA_CONF:-}" ]; then
    not_world_writable() { local mode; mode=$(stat -c '%a' "$QA_CONF"); (( (8#$mode & 2) == 0 )); }
    check "Учебный конфиг не world-writable" not_world_writable
fi
finish
