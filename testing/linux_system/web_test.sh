#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
URL="${1:-http://127.0.0.1:8080}"
code_is() { test "$(curl -sS -o /dev/null -w '%{http_code}' --max-time 3 "$URL$1")" = "$2"; }
check "Главная 200" code_is / 200
check "robots.txt 200" code_is /robots.txt 200
check "Отсутствующий путь 404" code_is /nonexist 404
check "favicon.ico 200" code_is /favicon.ico 200
seconds="$(curl -fsS -o /dev/null -w '%{time_total}' --max-time 3 "$URL/")" || seconds=999
check "Время ответа меньше 2 секунд" awk -v t="$seconds" 'BEGIN{exit !(t<2)}'
echo "response_time_seconds=$seconds"
finish
