#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
check "JSON orders" python3 "$ROOT/validate.py" orders "$DATA/orders.json"
finish
