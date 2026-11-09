#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
port_open() { timeout 2 bash -c 'exec 3<>/dev/tcp/127.0.0.1/$1' bash "$1"; }
port_closed() { ! port_open "$1"; }
check "Первый порт открыт" port_open "${QA_PORT1:-8080}"
check "Второй порт открыт" port_open "${QA_PORT2:-8081}"
check "Контрольный порт закрыт" port_closed "${QA_CLOSED_PORT:-9999}"
check "Первый HTTP доступен" curl -fsS --max-time 3 "http://127.0.0.1:${QA_PORT1:-8080}/"
check "Первый порт в ss" bash -c 'ss -tlnH | grep -qE ":$1[[:space:]]"' bash "${QA_PORT1:-8080}"
check "Второй порт в ss" bash -c 'ss -tlnH | grep -qE ":$1[[:space:]]"' bash "${QA_PORT2:-8081}"
finish
