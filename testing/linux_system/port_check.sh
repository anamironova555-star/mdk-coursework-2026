#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
for port in 22 80 443 3306 5432; do
    if timeout 2 bash -c 'exec 3<>/dev/tcp/127.0.0.1/$1' bash "$port" 2>/dev/null; then
        echo "OPEN: 127.0.0.1:$port"
    else
        echo "CLOSED: 127.0.0.1:$port"
    fi
done
