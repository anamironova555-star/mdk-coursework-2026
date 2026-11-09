#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
cd "${QA_BACKUP:?Укажите QA_BACKUP}"
archive_has() { local list; list="$(tar -tzf backup.tar.gz)" || return 1; [[ "$list" == *"source/$1"* ]]; }
file_count() { local list; list="$(tar -tzf backup.tar.gz)" || return 1; test "$(printf '%s\n' "$list" | grep -c '\.txt$')" -eq 3; }
check "Архив существует" test -s backup.tar.gz
check "gzip не повреждён" gzip -t backup.tar.gz
check "SHA256 совпадает" sha256sum -c backup.sha256
check "Есть users.txt" archive_has users.txt
check "Есть orders.txt" archive_has orders.txt
check "Есть products.txt" archive_has products.txt
check "Три файла" file_count
finish
