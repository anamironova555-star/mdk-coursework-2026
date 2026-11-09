#!/usr/bin/env bash
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
result=0
for script in os_check.sh port_check.sh integrity_check.sh log_check.sh; do bash "$ROOT/$script" || result=1; done
bash "$ROOT/web_test.sh" "${QA_URL_BASE:-http://127.0.0.1:8080}" || result=1
bash "$ROOT/load_test.sh" "${QA_URL_BASE:-http://127.0.0.1:8080}" 20 || result=1
exit "$result"
