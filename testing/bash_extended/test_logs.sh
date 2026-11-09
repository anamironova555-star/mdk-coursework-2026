#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
FILE="$DATA/app.log"
error_count() { test "$(grep -c ' ERROR ' "$FILE")" -eq 3; }
warn_count() { test "$(grep -c ' WARN ' "$FILE")" -eq 2; }
no_fatal() { ! grep -q FATAL "$FILE"; }
check "Лог существует" test -s "$FILE"
check "Три ERROR" error_count
check "Два WARN" warn_count
check "Событие запуска" grep -q 'Сервер запущен' "$FILE"
check "Нет FATAL" no_fatal
check "Дата в каждой строке" awk '$1 !~ /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$/{bad=1} END{exit bad}' "$FILE"
awk '{count[$3]++} END{for(k in count)print k,count[k]}' "$FILE" | sort
finish
