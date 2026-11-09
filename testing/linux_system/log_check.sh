#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
if command -v journalctl >/dev/null; then journalctl -p err -n 10 --no-pager 2>/dev/null || true; fi
found=0
for file in /var/log/secure /var/log/auth.log; do
    if [ -r "$file" ]; then
        echo "Неудачные логины: $(grep -ic 'failed password' "$file" || true)"
        found=1
    fi
done
if [ "$found" -eq 0 ]; then echo "SKIP: журналы secure/auth.log недоступны"; fi
du -sh /var/log 2>/dev/null || true
if [ -n "${QA_APP_LOG:-}" ]; then
    clean_log() { test -r "$QA_APP_LOG" && ! grep -qiE 'ERROR|FATAL' "$QA_APP_LOG"; }
    check "Нет ERROR/FATAL в учебном журнале" clean_log
fi
finish
