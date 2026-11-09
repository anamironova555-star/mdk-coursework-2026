#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
cat /etc/os-release
uname -r
df -h /
cat /proc/loadavg
if [ -f /etc/rosa-release ]; then cat /etc/rosa-release; else echo "WARN: /etc/rosa-release отсутствует; это другой дистрибутив"; fi
for svc in sshd crond NetworkManager; do
    if systemctl is-active --quiet "$svc" 2>/dev/null; then
        echo "PASS: Сервис $svc активен"
    else
        echo "WARN: Сервис $svc не активен или systemd недоступен"
    fi
done
if command -v rpm >/dev/null; then
    echo "INFO: rpm доступен; rpm -Va запускается вручную на РОСА"
else
    echo "SKIP: rpm -Va — на стенде нет RPM"
fi
