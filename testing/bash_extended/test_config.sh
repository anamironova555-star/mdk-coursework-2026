#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
CONF="$DATA/app.conf"
no_empty() { ! grep -qE '^[a-z]+=[[:space:]]*$' "$CONF"; }
server_port() { awk '/^\[/{section=$0} section=="[server]" && /^port=/{split($0,p,"="); found=1; if(p[2]!=8080)bad=1} END{exit (!found||bad)}' "$CONF"; }
check "Конфиг существует" test -s "$CONF"
check "Секция server" grep -q '^\[server\]$' "$CONF"
check "Секция database" grep -q '^\[database\]$' "$CONF"
check "Порт server = 8080" server_port
check "Уровень INFO" grep -q '^level=INFO$' "$CONF"
check "Путь абсолютный" grep -q '^file=/' "$CONF"
check "Нет пустых значений" no_empty
finish
