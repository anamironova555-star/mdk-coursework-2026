#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
FILE="$DATA/users.csv"
rows() { test "$(wc -l < "$FILE")" -eq 5; }
unique_column() { test -z "$(tail -n +2 "$FILE" | cut -d, -f"$1" | sort | uniq -d)"; }
check "CSV существует" test -s "$FILE"
check "Заголовок" grep -q '^id,name,email,age$' "$FILE"
check "Четыре записи" rows
check "Каждая строка содержит 4 поля" awk -F, 'NF!=4{bad=1} END{exit bad}' "$FILE"
check "ID уникальны" unique_column 1
check "Email уникальны" unique_column 3
check "Email содержит @" awk -F, 'NR>1 && $3 !~ /@/{bad=1} END{exit bad}' "$FILE"
check "Возраст целочисленный" awk -F, 'NR>1 && $4 !~ /^[0-9]+$/{bad=1} END{exit bad}' "$FILE"
finish
