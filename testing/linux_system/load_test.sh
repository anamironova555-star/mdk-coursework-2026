#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
URL="${1:-http://127.0.0.1:8080}"
N="${2:-20}"
if ! [[ "$N" =~ ^[1-9][0-9]*$ ]] || [ "$N" -gt 100 ]; then echo "N должно быть от 1 до 100"; exit 2; fi
start=$(date +%s%N)
OK=0
ERR=0
for ((i=0; i<N; i++)); do
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "$URL")
    if [ "$code" = 200 ]; then OK=$((OK+1)); else ERR=$((ERR+1)); fi
done
end=$(date +%s%N)
duration=$(((end-start)/1000000))
echo "requests=$N success=$OK errors=$ERR duration_ms=$duration mean_ms=$((duration/N))"
check "Все запросы успешны" test "$ERR" -eq 0
finish
