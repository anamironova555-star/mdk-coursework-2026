#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN="${QA_RUN:-$ROOT/.logs}"
mkdir -p "$RUN"
URL="${1:-https://example.com}"
PASS=0
FAIL=0
run_case() {
    local id="$1" path="$2" expected="$3" code
    code=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 5 "$URL$path")
    if [ "$code" = "$expected" ]; then
        echo "PASS $id $path expected=$expected actual=$code"
        PASS=$((PASS+1))
    else
        echo "FAIL $id $path expected=$expected actual=$code"
        FAIL=$((FAIL+1))
    fi
}
run_case TC-01 / 200
run_case TC-02 /not-found-xyz 404
run_case TC-03 /robots.txt 200
run_case TC-04 /favicon.ico 200
run_case TC-05 /redirect 302
echo "TOTAL=$((PASS+FAIL)) PASS=$PASS FAIL=$FAIL"
test "$FAIL" -eq 0
