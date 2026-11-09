#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
check "JSON products" python3 "$ROOT/validate.py" products "$DATA/products.json"
finish
