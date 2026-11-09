#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
if ! command -v jq >/dev/null; then
    echo "SKIP: jq отсутствует; необязательная зависимость"
    exit 0
fi
check "jq: синтаксис" jq empty "$DATA/users.json"
check "jq: 3 пользователя" jq -e '.users | length == 3' "$DATA/users.json"
check "jq: порт 8080" jq -e '.server.port == 8080' "$DATA/config.json"
finish
